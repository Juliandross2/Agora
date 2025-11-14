import React, { useEffect, useState, useMemo } from 'react';
import { useSnackbar } from 'notistack';
import { ArrowLeft, Edit2, Trash2, Eye } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { 
  listarProgramas, 
  buscarProgramas, 
  crearPrograma, 
  actualizarPrograma, 
  eliminarPrograma 
} from '../services/consumers/ProgramaClient';
import { obtenerEstadisticasPensum, crearPensum } from '../services/consumers/PensumClient';
import type { PensumEstadisticas } from '../services/domain/PensumModels';
import type { Programa } from '../services/domain/ProgramaModels';
import ProgramaFormDialog from '../components/ProgramaFormDialog';
import ConfirmDialog from '../components/ConfirmDialog';

export default function GestionProgramas() {
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const [programs, setPrograms] = useState<Programa[]>([]);
  const [allPrograms, setAllPrograms] = useState<Programa[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  // pensum stats cache: programa_id -> PensumEstadisticas | null
  const [pensumStats, setPensumStats] = useState<Record<number, PensumEstadisticas | null>>({});
  const [loadingPensum, setLoadingPensum] = useState<Record<number, boolean>>({});

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [formMode, setFormMode] = useState<'create' | 'edit'>('create');
  const [selectedPrograma, setSelectedPrograma] = useState<Programa | null>(null);

  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const [selectedProgramaId, setSelectedProgramaId] = useState<number | null>(null);

  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [programaToDelete, setProgramaToDelete] = useState<Programa | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  // refs to avoid refetching
  const fetchedRef = React.useRef<Set<number>>(new Set());
  const fetchingRef = React.useRef<Set<number>>(new Set());

  const [currentPage, setCurrentPage] = useState(1);
  const PAGE_SIZE = 5;

  // moved up: totalPages y displayedPrograms deben estar antes del useEffect que las consume
  const totalPages = useMemo(() => Math.max(1, Math.ceil(programs.length / PAGE_SIZE)), [programs.length, PAGE_SIZE]);
  const displayedPrograms = useMemo(() => {
    const start = (currentPage - 1) * PAGE_SIZE;
    return programs.slice(start, start + PAGE_SIZE);
  }, [programs, currentPage, PAGE_SIZE]);

  useEffect(() => {
    loadProgramas();
  }, []);

  const loadProgramas = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await listarProgramas();
      setAllPrograms(Array.isArray(res.programas) ? res.programas : []);
      setPrograms(Array.isArray(res.programas) ? res.programas : []);
      setCurrentPage(1);
      // reset pensum caches so new list will trigger re-fetch
      setPensumStats({});
      fetchedRef.current.clear();
      fetchingRef.current.clear();
      enqueueSnackbar('Programas cargados', { variant: 'success' });
    } catch (err: any) {
      const msg = err?.message || 'Error al cargar programas';
      setError(msg);
      enqueueSnackbar(msg, { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    setCurrentPage(1);

    if (!query.trim()) {
      setPrograms(allPrograms);
      return;
    }

    try {
      const res = await buscarProgramas(query);
      setPrograms(Array.isArray(res.programas) ? res.programas : []);
      enqueueSnackbar(`${res.programas?.length ?? 0} resultados para "${query}"`, { variant: 'info' });
    } catch (err: any) {
      const msg = err?.message || 'Error al buscar programas';
      console.error('Error searching:', err);
      setPrograms([]);
      enqueueSnackbar(msg, { variant: 'error' });
    }
  };

  // Fetch pensum statistics for visible programs (uses programa.pensum_activo_id)
  useEffect(() => {
    let mounted = true;

    const fetchFor = async (program: Programa) => {
      const pid = program.programa_id;
      // skip if already fetched or in progress
      if (fetchedRef.current.has(pid) || fetchingRef.current.has(pid)) return;

      fetchingRef.current.add(pid);
      setLoadingPensum((s) => ({ ...s, [pid]: true }));

      try {
        const pensumId = (program as any).pensum_activo_id ?? null;
        if (!pensumId) {
          // mark explicitly as no pensum
          if (!mounted) return;
          setPensumStats((s) => ({ ...s, [pid]: null }));
        } else {
          try {
            const stats = await obtenerEstadisticasPensum(pensumId);
            if (!mounted) return;
            setPensumStats((s) => ({ ...s, [pid]: stats }));
          } catch (err) {
            if (!mounted) return;
            setPensumStats((s) => ({ ...s, [pid]: null }));
          }
        }
      } finally {
        fetchingRef.current.delete(pid);
        fetchedRef.current.add(pid);
        if (mounted) setLoadingPensum((s) => ({ ...s, [pid]: false }));
      }
    };

    displayedPrograms.forEach((p) => fetchFor(p));

    return () => { mounted = false; };
  }, [displayedPrograms]);

  const handleCreate = () => {
    setFormMode('create');
    setSelectedPrograma(null);
    setIsFormOpen(true);
  };

  // Navegar a gestión de electivas. Si se pasa programaId se filtra por ese programa.
  const handleGestionElectivas = (programaId?: number) => {
    if (typeof programaId === 'number') {
      console.log("Navegando hacia gestion electivas con programaID", programaId);
      navigate(`/gestion-electivas?programaId=${programaId}`);
    } else {
      navigate('/gestion-electivas');
    }
  };
  const handleEdit = (programa: Programa) => {
    setFormMode('edit');
    setSelectedPrograma(programa);
    setIsFormOpen(true);
  };

  const handleFormSubmit = async (data: { nombre_programa: string; programa_id?: number }) => {
    if (formMode === 'create') {
      try {
        await crearPrograma({ nombre_programa: data.nombre_programa });
        enqueueSnackbar('Programa creado correctamente', { variant: 'success' });
      } catch (err: any) {
        const msg = err?.message || 'Error al crear el programa';
        enqueueSnackbar(msg, { variant: 'error' });
        throw err;
      }
    } else if (data.programa_id) {
      try {
        await actualizarPrograma(data.programa_id, { nombre_programa: data.nombre_programa });
        enqueueSnackbar('Programa actualizado correctamente', { variant: 'success' });
      } catch (err: any) {
        const msg = err?.message || 'Error al actualizar el programa';
        enqueueSnackbar(msg, { variant: 'error' });
        throw err;
      }
    }
    await loadProgramas();
  };

  const handleDeleteClick = (programa: Programa) => {
    setProgramaToDelete(programa);
    setIsDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!programaToDelete) return;

    try {
      await eliminarPrograma(programaToDelete.programa_id);
      await loadProgramas();
      setIsDeleteDialogOpen(false);
      setProgramaToDelete(null);
      enqueueSnackbar('Programa eliminado correctamente', { variant: 'success' });
    } catch (err: any) {
      const msg = err?.message || 'Error al eliminar el programa';
      enqueueSnackbar(msg, { variant: 'error' });
    }
  };

  const handleVerPensum = (programa: Programa) => {
    navigate(`/pensum/${programa.programa_id}`);
  };

  // Crea un pensum automáticamente (sin UI adicional) y redirige a la vista del pensum creado.
  const handleAutoCrearPensum = async (programa: Programa, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    const pid = programa.programa_id;
    // evitar duplicate clicks
    if (loadingPensum[pid]) return;

    setLoadingPensum((s) => ({ ...s, [pid]: true }));

    try {
      const payload = {
        programa_id: pid,
        anio_creacion: new Date().getFullYear(),
        es_activo: true,
      };

      const res = await crearPensum(payload);
      enqueueSnackbar(res.message || 'Pensum creado correctamente', { variant: 'success' });

      // intentar obtener estadísticas del pensum recién creado para actualizar UI
      try {
        const stats = await obtenerEstadisticasPensum(res.pensum.pensum_id);
        setPensumStats((s) => ({ ...s, [pid]: stats }));
      } catch {
        setPensumStats((s) => ({ ...s, [pid]: null }));
      }

      // refrescar lista de programas para que el backend devuelva pensum_activo_id actualizado
      await loadProgramas();

      // redirigir a la vista del pensum actual del programa
      navigate(`/pensum/${pid}`);
    } catch (err: any) {
      const msg = err?.message || 'Error al crear pensum';
      enqueueSnackbar(msg, { variant: 'error' });
    } finally {
      setLoadingPensum((s) => ({ ...s, [pid]: false }));
      fetchedRef.current.add(pid);
    }
  };

  const goToPage = (p: number) => {
    const page = Math.min(Math.max(1, p), totalPages);
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  return (
        <div className="min-h-screen bg-gray-50">
          <div className="bg-white border-b border-gray-200 px-8 py-6">
            <div className="flex items-center gap-4 mb-4">
              <button
                onClick={() => navigate('/')}
                className="text-blue-900 hover:text-blue-700 transition flex items-center gap-2"
              >
                <ArrowLeft size={20} />
                <span className="font-medium">Volver</span>
              </button>
            </div>
            <h1 className="text-3xl font-bold text-blue-900">Gestión de Programas</h1>
          </div>

          <div className="p-8">
            <div className="flex gap-4 mb-6">
              <input
                type="text"
                placeholder="Buscar programas..."
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <div className="flex items-center gap-2">
                <button
                  onClick={handleCreate}
                  className="px-6 py-3 bg-blue-900 text-white rounded-lg hover:bg-blue-800 transition font-medium"
                >
                  + Agregar
                </button>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Programa</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Pensum</th>
                    <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {loading && (
                    <tr>
                      <td colSpan={3} className="px-6 py-12 text-center text-gray-600">
                        Cargando programas...
                      </td>
                    </tr>
                  )}

                  {error && (
                    <tr>
                      <td colSpan={3} className="px-6 py-12 text-center text-red-600">
                        {error}
                      </td>
                    </tr>
                  )}

                  {!loading && !error && displayedPrograms.length === 0 && (
                    <tr>
                      <td colSpan={3} className="px-6 py-12 text-center text-gray-600">
                        No se encontraron programas
                      </td>
                    </tr>
                  )}

                  {!loading && !error && displayedPrograms.map((program) => (
                    <tr key={program.programa_id} className="border-b border-gray-100 hover:bg-gray-50 transition">
                      <td className="px-6 py-4">
                        <div>
                          <div className="font-medium text-gray-900">{program.nombre_programa}</div>
                          <div className="text-sm text-gray-500">
                            {loadingPensum[program.programa_id] ? (
                              'Cargando pensum...'
                            ) : pensumStats[program.programa_id] ? (
                              `${pensumStats[program.programa_id]!.creditos_obligatorios_totales} Créditos obligatorios • ${pensumStats[program.programa_id]!.total_materias} materias`
                            ) : (
                              'No tiene pensum activo'
                            )}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        {loadingPensum[program.programa_id] ? (
                          <span className="text-sm text-gray-500">Cargando...</span>
                        ) : pensumStats[program.programa_id] ? (
                          <button 
                            onClick={() => handleVerPensum(program)}
                            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition text-sm font-medium"
                          >
                            Ver
                          </button>
                        ) : (
                          <button
                            onClick={(e) => handleAutoCrearPensum(program, e)}
                            className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition text-sm font-medium"
                            disabled={!!loadingPensum[program.programa_id]}
                          >
                            {loadingPensum[program.programa_id] ? 'Creando...' : 'Añadir pensum'}
                          </button>
                        )}
                        { /* Botón por-programa para ir a la gestión de electivas de ese programa */ }
                        <button
                          onClick={() => handleGestionElectivas(program.programa_id)}
                          className="ml-3 px-3 py-2 bg-white border border-blue-900 text-blue-900 rounded-lg hover:bg-blue-50 transition text-sm font-medium"
                          title={`Ver electivas de ${program.nombre_programa}`}
                        >
                          Electivas
                        </button>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center justify-center gap-2">
                          <button
                            onClick={() => handleEdit(program)}
                            className="w-10 h-10 bg-blue-900 text-white rounded-full flex items-center justify-center hover:bg-blue-800 transition"
                            title="Editar"
                          >
                            <Edit2 size={18} />
                          </button>
                          <button
                            onClick={() => handleDeleteClick(program)}
                            className="w-10 h-10 bg-red-600 text-white rounded-full flex items-center justify-center hover:bg-red-700 transition"
                            title="Eliminar"
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {!loading && !error && programs.length > 0 && (
              <div className="mt-6 flex items-center justify-between">
                <div className="text-sm text-gray-600">
                  Mostrando {displayedPrograms.length} de {programs.length} programas
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => goToPage(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                  >
                    ←
                  </button>

                  <div className="flex items-center gap-1">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
                      <button
                        key={p}
                        onClick={() => goToPage(p)}
                        className={`w-10 h-10 rounded-lg font-medium transition ${
                          p === currentPage 
                            ? 'bg-blue-900 text-white' 
                            : 'hover:bg-gray-100 text-gray-700'
                        }`}
                      >
                        {p}
                      </button>
                    ))}
                  </div>

                  <button
                    onClick={() => goToPage(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                  >
                    →
                  </button>
                </div>
              </div>
            )}
          </div>

          <ProgramaFormDialog
            isOpen={isFormOpen}
            onClose={() => setIsFormOpen(false)}
            onSubmit={handleFormSubmit}
            programa={selectedPrograma}
            mode={formMode}
          />

          <ConfirmDialog
            isOpen={isDeleteDialogOpen}
            onCancel={() => setIsDeleteDialogOpen(false)}
            onConfirm={handleDeleteConfirm}
            title="Eliminar Programa"
            description={`¿Está seguro de eliminar el programa "${programaToDelete?.nombre_programa}"? Esta acción no se puede deshacer.`}
            confirmLabel="Eliminar"
            cancelLabel="Cancelar"
          />
        </div>
  );
}