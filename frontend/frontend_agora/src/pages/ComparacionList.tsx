import React, { useState, useEffect } from 'react';
import { Search, Download, Plus, FileSpreadsheet, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useSnackbar } from 'notistack';
import type { ComparacionEstudiante } from '../services/consumers/ComparacionClient';
import { exportComparacionResumenToPDF, exportComparacionPensumMatrixToExcel } from '../utils/exportUtils';
import { obtenerResultadosComparacion, type ComparacionResultadosCache } from '../utils/storageUtils';

type EstadoFiltro = 'TODOS' | 'APTO' | 'NO_APTO';

export default function ComparacionList() {
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  
  const [searchTerm, setSearchTerm] = useState('');
  const [filtroEstado, setFiltroEstado] = useState<EstadoFiltro>('TODOS');
  const [cache, setCache] = useState<ComparacionResultadosCache | null>(null);

  useEffect(() => {
    // Intentar obtener resultados desde sessionStorage
    const resultadosGuardados = obtenerResultadosComparacion();
    if (resultadosGuardados) {
      setCache(resultadosGuardados);
    }
  }, []);

  if (!cache) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-blue-900 text-white py-6">
          <div className="max-w-6xl mx-auto px-6">
            <h1 className="text-xl font-semibold text-center">Resultados de Comparación</h1>
          </div>
        </div>
        <div className="p-8 text-center">
          <div className="max-w-md mx-auto">
            <div className="text-gray-400 mb-4">
              <Search className="w-16 h-16 mx-auto mb-4" />
            </div>
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              No hay comparaciones disponibles
            </h3>
            <p className="text-gray-500 mb-6">
              Realiza tu primera comparación de pensum para ver los resultados aquí.
            </p>
            <button
              onClick={() => navigate('/comparacion')}
              className="bg-blue-900 text-white px-6 py-3 rounded-md hover:bg-blue-800 transition flex items-center gap-2 mx-auto"
            >
              <Plus className="w-4 h-4" />
              Nueva Comparación
            </button>
          </div>
        </div>
      </div>
    );
  }

  const resultados = cache.response;
  const metadata = cache.metadata;
  const pensumMaterias = metadata?.pensumMaterias ?? [];
  const semestreLimite = metadata?.semestreLimite ?? null;
  const estudiantesOrdenados = [...resultados.resultados].sort(
    (a, b) => a.porcentaje_avance - b.porcentaje_avance
  );

  // Filtrar estudiantes
  const estudiantesFiltrados = estudiantesOrdenados.filter(estudiante => {
    const matchesSearch = estudiante.estudiante.toLowerCase().includes(searchTerm.toLowerCase());
    const esApto = estudiante.estado === 1;
    const matchesEstado = 
      filtroEstado === 'TODOS' || 
      (filtroEstado === 'APTO' && esApto) ||
      (filtroEstado === 'NO_APTO' && !esApto);
    return matchesSearch && matchesEstado;
  });

  const porcentajeAptos = resultados.total_estudiantes > 0 
    ? ((resultados.elegibles / resultados.total_estudiantes) * 100).toFixed(1) 
    : '0';
  const porcentajeNoAptos = resultados.total_estudiantes > 0 
    ? ((resultados.no_elegibles / resultados.total_estudiantes) * 100).toFixed(1) 
    : '0';

  const handleVerDetalle = (estudiante: ComparacionEstudiante) => {
    navigate(`/comparacion-detalle/${estudiante.estudiante}`, { 
      state: { estudiante } 
    });
  };

  const handleExportarPDF = async () => {
    try {
      exportComparacionResumenToPDF(estudiantesOrdenados);
      enqueueSnackbar('PDF generado correctamente', { variant: 'success' });
    } catch (error) {
      console.error('Error al exportar PDF:', error);
      enqueueSnackbar('Error al generar el reporte PDF', { variant: 'error' });
    }
  };

  const handleExportarExcel = async () => {
    try {
      if (!pensumMaterias.length) {
        enqueueSnackbar('No hay información del pensum para generar el Excel. Repite la comparación.', { variant: 'warning' });
        return;
      }

      await exportComparacionPensumMatrixToExcel({
        estudiantes: estudiantesOrdenados,
        pensumMaterias,
        semestreLimite: semestreLimite ?? undefined,
        programaNombre: metadata?.programaNombre
      });
      enqueueSnackbar('Excel generado correctamente', { variant: 'success' });
    } catch (error) {
      console.error('Error al exportar Excel:', error);
      enqueueSnackbar('Error al generar el reporte Excel', { variant: 'error' });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header azul */}
      <div className="bg-blue-900 text-white py-6">
        <div className="max-w-6xl mx-auto px-6">
          <h1 className="text-xl font-semibold text-center">Resultados de Comparación</h1>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="max-w-6xl mx-auto p-6">
        {/* Barra de búsqueda y filtros */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
          <div className="flex flex-col lg:flex-row gap-4 items-center">
            {/* Búsqueda */}
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Buscar estudiante..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
            </div>

            {/* Filtros de estado */}
            <div className="flex gap-2">
              <button
                onClick={() => setFiltroEstado('TODOS')}
                className={`px-6 py-2 rounded-full font-medium transition ${
                  filtroEstado === 'TODOS'
                    ? 'bg-blue-900 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Todos
              </button>
              <button
                onClick={() => setFiltroEstado('APTO')}
                className={`px-6 py-2 rounded-full font-medium transition ${
                  filtroEstado === 'APTO'
                    ? 'bg-green-600 text-white'
                    : 'border border-green-600 text-green-600 hover:bg-green-50'
                }`}
              >
                Aptos
              </button>
              <button
                onClick={() => setFiltroEstado('NO_APTO')}
                className={`px-6 py-2 rounded-full font-medium transition ${
                  filtroEstado === 'NO_APTO'
                    ? 'bg-red-600 text-white'
                    : 'border border-red-600 text-red-600 hover:bg-red-50'
                }`}
              >
                No Aptos
              </button>
            </div>
          </div>
        </div>

        {/* Lista de estudiantes */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
          <h2 className="text-lg font-semibold text-blue-900 mb-4">Estudiantes Evaluados</h2>
          
          <div className="space-y-3">
            {estudiantesFiltrados.map((estudiante) => {
              const esApto = estudiante.estado === 1;
              const iniciales = estudiante.estudiante.substring(0, 2).toUpperCase();
              
              return (
                <div
                  key={estudiante.estudiante}
                  className={`flex items-center justify-between p-4 rounded-lg border transition hover:shadow-sm ${
                    esApto ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
                  }`}
                >
                  <div className="flex items-center gap-4">
                    {/* Avatar */}
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-white ${
                      esApto ? 'bg-green-600' : 'bg-red-600'
                    }`}>
                      {iniciales}
                    </div>
                    
                    {/* Info del estudiante */}
                    <div>
                      <div className="font-medium text-gray-900">Estudiante {estudiante.estudiante}</div>
                      <div className="text-sm text-gray-500">
                        Semestre {estudiante.semestre_maximo} • {estudiante.creditos_aprobados}/{estudiante.creditos_obligatorios_totales} créditos
                      </div>
                      <div className={`text-sm font-medium ${
                        esApto ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {esApto 
                          ? `APTO (${estudiante.porcentaje_avance.toFixed(1)}% completado)`
                          : `NO APTO (${estudiante.porcentaje_avance.toFixed(1)}% completado)`
                        }
                      </div>
                    </div>
                  </div>

                  {/* Botón Ver */}
                  <button
                    onClick={() => handleVerDetalle(estudiante)}
                    className="bg-blue-900 text-white px-6 py-2 rounded-md hover:bg-blue-800 transition"
                  >
                    Ver
                  </button>
                </div>
              );
            })}
          </div>
        </div>

        {/* Resumen General */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
          <h2 className="text-lg font-semibold text-blue-900 mb-4">Resumen General</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Total evaluados: </span>
              <span className="font-semibold">{resultados.total_estudiantes} estudiantes</span>
            </div>
            <div>
              <span className="text-gray-600">Aptos: </span>
              <span className="font-semibold text-green-600">{resultados.elegibles} ({porcentajeAptos}%)</span>
            </div>
            <div>
              <span className="text-gray-600">No aptos: </span>
              <span className="font-semibold text-red-600">{resultados.no_elegibles} ({porcentajeNoAptos}%)</span>
            </div>
          </div>
        </div>

        {/* Botones de acción */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/comparacion')}
            className="flex items-center justify-center gap-2 px-8 py-3 border border-blue-900 text-blue-900 rounded-md hover:bg-blue-50 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            Volver
          </button>
          <button
            onClick={handleExportarPDF}
            className="flex items-center justify-center gap-2 px-8 py-3 border border-blue-900 text-blue-900 rounded-md hover:bg-blue-50 transition"
          >
            <Download className="w-4 h-4" />
            Exportar PDF
          </button>
          <button
            onClick={handleExportarExcel}
            className="flex items-center justify-center gap-2 px-8 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 transition"
          >
            <FileSpreadsheet className="w-4 h-4" />
            Exportar Excel
          </button>
          <button
            onClick={() => navigate('/comparacion')}
            className="flex items-center justify-center gap-2 px-8 py-3 bg-blue-900 text-white rounded-md hover:bg-blue-800 transition"
          >
            <Plus className="w-4 h-4" />
            Nueva Comparación
          </button>
        </div>
      </div>
    </div>
  );
}