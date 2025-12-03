import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { ArrowLeft, Download, FileSpreadsheet } from 'lucide-react';
import { useSnackbar } from 'notistack';
import type { ComparacionEstudiante } from '../services/consumers/ComparacionClient';
import { exportComparacionDetalleToPDF, exportComparacionDetalleToExcel } from '../utils/exportUtils';

export default function ComparacionDetailView() {
  const navigate = useNavigate();
  const location = useLocation();
  const { enqueueSnackbar } = useSnackbar();
  
  const state = location.state as { estudiante?: ComparacionEstudiante };
  const estudiante = state?.estudiante;

  if (!estudiante) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-blue-900 text-white py-6">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <h1 className="text-xl font-semibold">Detalle de Comparación</h1>
          </div>
        </div>
        <div className="p-8 text-center">
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            Estudiante no encontrado
          </h3>
          <p className="text-gray-500 mb-4">
            No se encontró información para este estudiante
          </p>
          <button
            onClick={() => navigate('/comparacion-resultados')}
            className="bg-blue-900 text-white px-6 py-3 rounded-md hover:bg-blue-800 transition"
          >
            Volver a resultados
          </button>
        </div>
      </div>
    );
  }

  const esApto = estudiante.estado === 1;

  const handleGenerarReportePDF = async () => {
    try {
      exportComparacionDetalleToPDF(estudiante);
      enqueueSnackbar('PDF generado correctamente', { variant: 'success' });
    } catch (error) {
      console.error('Error al generar el reporte PDF:', error);
      enqueueSnackbar('Error al generar el reporte PDF', { variant: 'error' });
    }
  };

  const handleGenerarReporteExcel = async () => {
    try {
      exportComparacionDetalleToExcel(estudiante);
      enqueueSnackbar('Excel generado correctamente', { variant: 'success' });
    } catch (error) {
      console.error('Error al generar el reporte Excel:', error);
      enqueueSnackbar('Error al generar el reporte Excel', { variant: 'error' });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header azul oscuro */}
      <div className="bg-blue-900 text-white py-6">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h1 className="text-xl font-semibold">Comparación de Pensum</h1>
        </div>
      </div>

      {/* Header azul claro */}
      <div className="bg-blue-400 text-white py-4">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-lg font-semibold">Detalle de Comparación</h2>
          <h3 className="text-base">Estudiante {estudiante.estudiante}</h3>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="max-w-4xl mx-auto p-6">
        {/* Info del estudiante */}
        <div className="bg-gray-100 rounded-lg p-4 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-semibold">Código:</span> {estudiante.estudiante}
            </div>
            <div>
              <span className="font-semibold">Semestre máximo:</span> {estudiante.semestre_maximo}
            </div>
            <div>
              <span className="font-semibold">Créditos aprobados:</span> {estudiante.creditos_aprobados}/{estudiante.creditos_obligatorios_totales}
            </div>
            <div>
              <span className="font-semibold">Períodos matriculados:</span> {estudiante.periodos_matriculados}
            </div>
            <div>
              <span className="font-semibold">Avance:</span> {estudiante.porcentaje_avance.toFixed(1)}%
            </div>
            <div>
              <span className="font-semibold">Nivelado:</span> {estudiante.nivelado ? 'Sí' : 'No'}
            </div>
          </div>
        </div>

        {/* Materias faltantes */}
        {estudiante.materias_faltantes_hasta_semestre_limite.length > 0 && (
          <div className="bg-white rounded-lg border p-6 mb-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-4">
              Materias Faltantes hasta Semestre {estudiante.semestre_maximo}
            </h3>
            
            <div className="space-y-2">
              {estudiante.materias_faltantes_hasta_semestre_limite.map((materia, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-3 p-3 rounded-lg border border-red-200 bg-red-50"
                >
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <span className="font-medium capitalize">{materia}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Resumen */}
        <div className="bg-gray-100 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-blue-900 mb-2">Resumen:</h3>
          <div className="space-y-1 text-sm">
            <div className="text-green-600">
              ✓ Créditos aprobados: {estudiante.creditos_aprobados}
            </div>
            <div className="text-red-600">
              ✗ Materias faltantes: {estudiante.materias_faltantes_hasta_semestre_limite.length}
            </div>
            <div className="text-gray-700">
              • Porcentaje de avance: {estudiante.porcentaje_avance.toFixed(1)}%
            </div>
          </div>
        </div>

        {/* Resultado final */}
        <div className={`rounded-lg p-4 mb-6 text-center font-semibold text-white ${
          esApto ? 'bg-green-600' : 'bg-red-600'
        }`}>
          <div className="text-sm uppercase tracking-wide">RESULTADO:</div>
          <div className="text-lg">
            El estudiante {esApto ? 'SÍ es apto' : 'NO es apto'} para electivas
          </div>
        </div>

        {/* Botones de acción */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/comparacion-resultados')}
            className="flex items-center justify-center gap-2 px-8 py-3 border border-blue-900 text-blue-900 rounded-md hover:bg-blue-50 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            Volver
          </button>
          <button
            onClick={handleGenerarReportePDF}
            className="flex items-center justify-center gap-2 px-8 py-3 bg-blue-900 text-white rounded-md hover:bg-blue-800 transition"
          >
            <Download className="w-4 h-4" />
            Generar PDF
          </button>
          <button
            onClick={handleGenerarReporteExcel}
            className="flex items-center justify-center gap-2 px-8 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 transition"
          >
            <FileSpreadsheet className="w-4 h-4" />
            Exportar a Excel
          </button>
        </div>
      </div>
    </div>
  );
}