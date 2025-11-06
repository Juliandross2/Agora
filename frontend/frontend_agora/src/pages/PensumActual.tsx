import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useSnackbar } from 'notistack';
import { obtenerPensumActual, obtenerMateriasPorSemestre } from '../services/consumers/PensumClient';
import type { PensumProgramaResponse, MateriaPorSemestre } from '../services/domain/PensumModels';
import { useActiveSection } from '../DashboardLayout';
import CardSemestreMaterias from '../components/CardSemestreMaterias';

export default function PensumActual() {
  const { programaId } = useParams();
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const { setActiveSection } = useActiveSection();

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
        <div className="flex items-center gap-4 mb-4">
          <button
            onClick={handleVolver}
            className="text-blue-900 hover:text-blue-700 transition flex items-center gap-2"
          >
            <ArrowLeft size={20} />
            <span className="font-medium">Volver</span>
          </button>
        </div>
        <h1 className="text-3xl font-bold text-blue-900">Pensum - {pensumData.programa_nombre}</h1>
      </div>

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

            {/* Grid de semestres con materias */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              {semestresConMaterias.map((semestreData) => (
                <CardSemestreMaterias
                  key={semestreData.semestre}
                  semestre={semestreData.semestre}
                  materias={semestreData.materias}
                  creditosTotales={semestreData.creditos_totales}
                />
              ))}
            </div>

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