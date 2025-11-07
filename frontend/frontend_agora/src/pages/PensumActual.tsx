import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useSnackbar } from 'notistack';
import { obtenerPensumActual, obtenerMateriasPorSemestre } from '../services/consumers/PensumClient';
import CrearMateriaFormDialog from '../components/CrearMateriaFormDialog';
import EditarMateriaFormDialog from '../components/EditarMateriaFormDialog';
import ContextMenu from '../components/ContextMenu';
import ConfirmDeleteDialog from '../components/ConfirmDeleteDialog';
import type { Materia as MateriaModel } from '../services/domain/PensumModels';
import type { PensumProgramaResponse, MateriaPorSemestre } from '../services/domain/PensumModels';
import { useActiveSection } from '../DashboardLayout';
import { DragDropContext, Droppable, Draggable, DropResult } from '@hello-pangea/dnd';
import { patchMateria, eliminarMateria } from '../services/consumers/MateriaClient';

export default function PensumActual() {
  const { programaId } = useParams();
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const { setActiveSection } = useActiveSection();

  const [crearMateriaOpen, setCrearMateriaOpen] = useState(false);
  const [editarMateriaOpen, setEditarMateriaOpen] = useState(false);
  const [selectedMateria, setSelectedMateria] = useState<MateriaModel | null>(null);
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; materia: MateriaModel } | null>(null);
  const [confirmDeleteOpen, setConfirmDeleteOpen] = useState(false);
  const [materiaToDelete, setMateriaToDelete] = useState<MateriaModel | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const [pensumData, setPensumData] = useState<PensumProgramaResponse | null>(null);
  const [materiasPorSemestre, setMateriasPorSemestre] = useState<MateriaPorSemestre[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingMaterias, setLoadingMaterias] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setActiveSection('programas');
  }, [setActiveSection]);

  useEffect(() => {
    if (!programaId) {
      setError('ID de programa no válido');
      return;
    }

    const loadPensum = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await obtenerPensumActual(parseInt(programaId));
        setPensumData(res);
        if (!res.pensum_actual) {
          enqueueSnackbar('No hay pensum activo para este programa', { variant: 'warning' });
        } else {
          enqueueSnackbar('Pensum cargado correctamente', { variant: 'success' });
          // Cargar materias si hay pensum activo
          await loadMaterias(res.pensum_actual.pensum_id);
        }
      } catch (err: any) {
        const msg = err?.message || 'Error al cargar el pensum';
        setError(msg);
        enqueueSnackbar(msg, { variant: 'error' });
      } finally {
        setLoading(false);
      }
    };

    loadPensum();
  }, [programaId, enqueueSnackbar]);

  const loadMaterias = async (pensumId: number) => {
    setLoadingMaterias(true);
    try {
      const materias = await obtenerMateriasPorSemestre(pensumId);
      setMateriasPorSemestre(materias);
    } catch (err: any) {
      console.warn('Error al cargar materias:', err?.message);
      // No mostrar error si las materias no están disponibles aún
      setMateriasPorSemestre([]);
    } finally {
      setLoadingMaterias(false);
    }
  };

  const handleVolver = () => {
    navigate('/gestion-programas');
  };
 
  const handleCrearMateriaSuccess = async (created?: MateriaModel) => {
    // refrescar materias si existe pensum activo
    const pensumId = pensumData?.pensum_actual?.pensum_id;
    if (pensumId) {
      await loadMaterias(pensumId);
    }

    // reconsultar el pensum para obtener métricas actualizadas (contador de electivas)
    if (programaId) {
      try {
        const updatedPensum = await obtenerPensumActual(parseInt(programaId, 10));
        setPensumData(updatedPensum);
      } catch (err) {
        console.warn('No se pudo actualizar el pensum después de crear materia', err);
      }
    }

    setCrearMateriaOpen(false);
  };

  const handleEditarMateriaSuccess = async (updated?: MateriaModel) => {
    const pensumId = pensumData?.pensum_actual?.pensum_id;
    if (pensumId) {
      await loadMaterias(pensumId);
    }
    setEditarMateriaOpen(false);
    setSelectedMateria(null);
  };

  const handleContextMenu = (e: React.MouseEvent, materia: MateriaModel) => {
    e.preventDefault();
    e.stopPropagation();
    setContextMenu({
      x: e.clientX,
      y: e.clientY,
      materia
    });
  };

  const handleEditMateria = () => {
    if (contextMenu) {
      setSelectedMateria(contextMenu.materia);
      setEditarMateriaOpen(true);
    }
  };

  const handleDeleteMateria = () => {
    if (contextMenu) {
      setMateriaToDelete(contextMenu.materia);
      setConfirmDeleteOpen(true);
    }
  };

  const confirmDelete = async () => {
    if (!materiaToDelete) return;
    setDeleteLoading(true);
    try {
      await eliminarMateria(materiaToDelete.materia_id);
      enqueueSnackbar('Materia eliminada correctamente', { variant: 'success' });
      const pensumId = pensumData?.pensum_actual?.pensum_id;
      if (pensumId) {
        await loadMaterias(pensumId);
      }
    } catch (err: any) {
      const msg = err?.message || 'Error al eliminar materia';
      enqueueSnackbar(msg, { variant: 'error' });
    } finally {
      setDeleteLoading(false);
      setConfirmDeleteOpen(false);
      setMateriaToDelete(null);
    }
  };

  // Handler para drag and drop
  const onDragEnd = async (result: DropResult) => {
    const { source, destination, draggableId } = result;
    
    // Si no hay destino o es la misma posición, no hacer nada
    if (!destination) return;
    if (source.droppableId === destination.droppableId && source.index === destination.index) return;

    // Extraer semestres de los droppableIds (formato: 'semestre-X')
    const sourceSemestre = parseInt(source.droppableId.replace('semestre-', ''), 10);
    const destinationSemestre = parseInt(destination.droppableId.replace('semestre-', ''), 10);
    const materiaId = parseInt(draggableId, 10);

    // Solo actualizar si cambia de semestre
    if (sourceSemestre !== destinationSemestre) {
      try {
        await patchMateria(materiaId, { semestre: destinationSemestre });
        enqueueSnackbar('Materia movida correctamente', { variant: 'success' });
        
        // Refrescar materias
        const pensumId = pensumData?.pensum_actual?.pensum_id;
        if (pensumId) {
          await loadMaterias(pensumId);
        }
      } catch (err: any) {
        const msg = err?.message || 'Error al mover materia';
        enqueueSnackbar(msg, { variant: 'error' });
        
        // Refrescar materias para evitar inconsistencias
        const pensumId = pensumData?.pensum_actual?.pensum_id;
        if (pensumId) {
          await loadMaterias(pensumId);
        }
      }
    }
  };
 
  // Generar array de 10 semestres con las materias correspondientes
  const semestresConMaterias = Array.from({ length: 10 }, (_, index) => {
    const semestre = index + 1;
    const materiasSemestre = materiasPorSemestre.find(m => m.semestre === semestre);
    return {
      semestre,
      materias: materiasSemestre?.materias || [],
      creditos_totales: materiasSemestre?.creditos_totales || 0
    };
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-lg text-gray-600">Cargando pensum...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-lg text-red-600 mb-4">{error}</div>
          <button
            onClick={handleVolver}
            className="px-6 py-3 bg-blue-900 text-white rounded-lg hover:bg-blue-800 transition"
          >
            Volver a Programas
          </button>
        </div>
      </div>
    );
  }

  if (!pensumData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-lg text-gray-600">No se encontró información del pensum</div>
        </div>
      </div>
    );
  }

  const pensum = pensumData.pensum_actual;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-8 py-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <button
              onClick={handleVolver}
              className="text-blue-900 hover:text-blue-700 transition flex items-center gap-2"
            >
              <ArrowLeft size={20} />
              <span className="font-medium">Volver</span>
            </button>
          </div>
          <div>
            <button
              onClick={() => setCrearMateriaOpen(true)}
              title="Crear materia"
              className="px-4 py-4 translate-y-8 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium"
            >
              + Crear materia
            </button>
          </div>
        </div>
        <h1 className="text-3xl font-bold text-blue-900">Pensum - {pensumData.programa_nombre}</h1>
      </div>
 
      <CrearMateriaFormDialog
        isOpen={crearMateriaOpen}
        onClose={() => setCrearMateriaOpen(false)}
        pensumId={pensum?.pensum_id ?? null}
        onCreated={handleCrearMateriaSuccess}
      />

      <EditarMateriaFormDialog
        isOpen={editarMateriaOpen}
        onClose={() => setEditarMateriaOpen(false)}
        materia={selectedMateria}
        onUpdated={handleEditarMateriaSuccess}
      />

      {contextMenu && (
        <ContextMenu
          x={contextMenu.x}
          y={contextMenu.y}
          onEdit={handleEditMateria}
          onDelete={handleDeleteMateria}
          onClose={() => setContextMenu(null)}
        />
      )}

      <ConfirmDeleteDialog
        isOpen={confirmDeleteOpen}
        onCancel={() => {
          setConfirmDeleteOpen(false);
          setMateriaToDelete(null);
        }}
        onConfirm={confirmDelete}
        loading={deleteLoading}
        materiaNombre={materiaToDelete?.nombre_materia}
      />

      <div className="p-8">
        {!pensum ? (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center">
            <div className="text-lg text-gray-600 mb-4">
              No hay pensum activo para este programa
            </div>
            <div className="text-sm text-gray-500">
              El programa "{pensumData.programa_nombre}" no tiene un pensum definido actualmente.
            </div>
          </div>
        ) : (
          <>
            {/* Header del pensum */}
            <div className="bg-gradient-to-r from-blue-900 to-blue-700 text-white rounded-xl p-6 mb-8">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold mb-2">{pensum.programa_nombre}</h2>
                  <div className="text-blue-100">
                    Pensum {pensum.anio_creacion} • {pensum.creditos_obligatorios_totales} créditos obligatorios • {pensum.total_materias_obligatorias} materias
                  </div>
                </div>
                <div className="bg-white/20 rounded-lg p-4 text-center">
                  <div className="text-3xl font-bold">{pensum.total_materias_electivas}</div>
                  <div className="text-sm text-blue-100">Materias Electivas</div>
                </div>
              </div>
            </div>

            {/* Leyenda */}
            <div className="bg-white rounded-lg p-4 mb-6 shadow-sm border">
              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-500 rounded"></div>
                  <span className="text-sm">Obligatoria</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-orange-500 rounded"></div>
                  <span className="text-sm">Electiva</span>
                </div>
              </div>
            </div>

            {/* Loading de materias */}
            {loadingMaterias && (
              <div className="bg-white rounded-lg p-6 mb-6 text-center">
                <div className="text-gray-600">Cargando materias del pensum...</div>
              </div>
            )}

            {/* Grid de semestres con materias - CON DRAG AND DROP */}
            <DragDropContext onDragEnd={onDragEnd}>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                {semestresConMaterias.map((semestreData) => (
                  <Droppable droppableId={`semestre-${semestreData.semestre}`} key={semestreData.semestre}>
                    {(provided, snapshot) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.droppableProps}
                        className={`bg-white rounded-lg shadow-sm border overflow-hidden ${
                          snapshot.isDraggingOver ? 'ring-2 ring-blue-300 bg-blue-50' : ''
                        }`}
                      >
                        <div className="bg-blue-900 text-white px-4 py-3">
                          <h3 className="font-semibold text-center">Semestre {semestreData.semestre}</h3>
                          <div className="text-xs text-blue-200 text-center">
                            {semestreData.creditos_totales > 0 ? `${semestreData.creditos_totales} créditos` : '0 créditos'}
                          </div>
                        </div>
                        <div className="p-4 space-y-3 min-h-[120px]">
                          {semestreData.materias.length === 0 ? (
                            <div className="text-center text-gray-400 py-4">
                              <div className="text-sm">Sin materias</div>
                            </div>
                          ) : (
                            semestreData.materias.map((materia, index) => (
                              <Draggable 
                                key={materia.materia_id} 
                                draggableId={materia.materia_id.toString()} 
                                index={index}
                              >
                                {(draggableProvided, draggableSnapshot) => (
                                  <div
                                    ref={draggableProvided.innerRef}
                                    {...draggableProvided.draggableProps}
                                    {...draggableProvided.dragHandleProps}
                                    onContextMenu={(e) => handleContextMenu(e, materia)}
                                    className={`border rounded p-3 cursor-move transition-all ${
                                      draggableSnapshot.isDragging 
                                        ? 'shadow-lg transform rotate-2 bg-white border-blue-300' 
                                        : ''
                                    } ${
                                      (materia as any).es_electiva
                                        ? 'bg-orange-50 border-orange-200'
                                        : 'bg-green-50 border-green-200'
                                    }`}
                                  >
                                    <div className={`font-medium text-sm ${
                                      (materia as any).es_electiva ? 'text-orange-800' : 'text-green-800'
                                    }`}>
                                      {materia.nombre_materia}
                                    </div>
                                    <div className={`text-xs ${
                                      (materia as any).es_electiva ? 'text-orange-600' : 'text-green-600'
                                    }`}>
                                      {materia.creditos} Créditos
                                    </div>
                                  </div>
                                )}
                              </Draggable>
                            ))
                          )}
                          {provided.placeholder}
                        </div>
                      </div>
                    )}
                  </Droppable>
                ))}
              </div>
            </DragDropContext>

            {/* Información adicional */}
            <div className="mt-8 bg-white rounded-lg p-6 shadow-sm border">
              <div className="text-center text-gray-500 text-sm">
                © {new Date().getFullYear()} Universidad del Cauca
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}