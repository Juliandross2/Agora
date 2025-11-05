import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Download, FileSpreadsheet } from 'lucide-react';
import DashboardLayout from '../DashboardLayout';
import { exportDetalleToPDF, exportDetalleToExcel } from '../utils/exportUtils';

interface Materia {
  id: string;
  nombre: string;
  estado: 'APROBADA' | 'NO_APROBADA' | 'NO_CURSADA';
  nota?: number;
}

interface DetalleEstudiante {
  id: string;
  nombre: string;
  programa: string;
  estado: 'APTO' | 'NO_APTO';
  materias: Materia[];
}

export default function ComparacionDetailView() {
  const navigate = useNavigate();
  const { estudianteId } = useParams();
  
  // Variable debug para mostrar datos de ejemplo
  const DEBUG_MODE = true;

  // Función para obtener datos del estudiante por ID (simulado)
  const getEstudianteById = (id: string): DetalleEstudiante | null => {
    const estudiantesDemo: { [key: string]: DetalleEstudiante } = {
      '12345': {
        id: '12345',
        nombre: 'Juan Pérez',
        programa: 'Ingeniería de Sistemas',
        estado: 'NO_APTO',
        materias: [
          { id: '1', nombre: 'Cálculo I', estado: 'APROBADA', nota: 4.2 },
          { id: '2', nombre: 'Programación I', estado: 'APROBADA', nota: 3.8 },
          { id: '3', nombre: 'Álgebra Lineal', estado: 'NO_APROBADA', nota: 2.1 },
          { id: '4', nombre: 'Cálculo II', estado: 'NO_CURSADA' },
          { id: '5', nombre: 'Física I', estado: 'NO_APROBADA', nota: 1.8 },
          { id: '6', nombre: 'Fundamentos de Ingeniería', estado: 'APROBADA', nota: 4.0 }
        ]
      },
      '12346': {
        id: '12346',
        nombre: 'María González',
        programa: 'Ingeniería de Sistemas',
        estado: 'APTO',
        materias: [
          { id: '1', nombre: 'Cálculo I', estado: 'APROBADA', nota: 4.5 },
          { id: '2', nombre: 'Programación I', estado: 'APROBADA', nota: 4.8 },
          { id: '3', nombre: 'Álgebra Lineal', estado: 'APROBADA', nota: 4.2 },
          { id: '4', nombre: 'Cálculo II', estado: 'APROBADA', nota: 4.0 },
          { id: '5', nombre: 'Física I', estado: 'APROBADA', nota: 3.9 },
          { id: '6', nombre: 'Fundamentos de Ingeniería', estado: 'APROBADA', nota: 4.3 }
        ]
      },
      '12347': {
        id: '12347',
        nombre: 'Carlos Rodríguez',
        programa: 'Ingeniería de Sistemas',
        estado: 'NO_APTO',
        materias: [
          { id: '1', nombre: 'Cálculo I', estado: 'APROBADA', nota: 3.5 },
          { id: '2', nombre: 'Programación I', estado: 'APROBADA', nota: 4.1 },
          { id: '3', nombre: 'Álgebra Lineal', estado: 'APROBADA', nota: 3.8 },
          { id: '4', nombre: 'Cálculo II', estado: 'APROBADA', nota: 3.2 },
          { id: '5', nombre: 'Física I', estado: 'NO_APROBADA', nota: 2.5 },
          { id: '6', nombre: 'Fundamentos de Ingeniería', estado: 'NO_CURSADA' }
        ]
      }
    };

    return estudiantesDemo[id] || null;
  };

  const estudiante = DEBUG_MODE ? getEstudianteById(estudianteId || '') : null;

  if (!estudiante) {
    return (
      <DashboardLayout>
        {() => (
          <div className="p-8 text-center">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              Estudiante no encontrado
            </h3>
            <p className="text-gray-500 mb-4">
              No se encontró información para el ID: {estudianteId}
            </p>
            <button
              onClick={() => navigate('/comparacion-resultados')}
              className="bg-blue-900 text-white px-6 py-3 rounded-md hover:bg-blue-800 transition"
            >
              Volver a resultados
            </button>
          </div>
        )}
      </DashboardLayout>
    );
  }

  // Calcular estadísticas
  const materiasAprobadas = estudiante.materias.filter(m => m.estado === 'APROBADA').length;
  const materiasNoAprobadas = estudiante.materias.filter(m => m.estado === 'NO_APROBADA').length;
  const materiasNoCursadas = estudiante.materias.filter(m => m.estado === 'NO_CURSADA').length;

  const handleVolver = () => {
    navigate('/comparacion-resultados');
  };

  const handleGenerarReportePDF = async () => {
    try {
      exportDetalleToPDF(estudiante);
    } catch (error) {
      console.error('Error al generar el reporte PDF:', error);
      alert('Error al generar el reporte PDF');
    }
  };

  const handleGenerarReporteExcel = async () => {
    try {
      exportDetalleToExcel(estudiante);
    } catch (error) {
      console.error('Error al generar el reporte Excel:', error);
      alert('Error al generar el reporte Excel');
    }
  };

  return (
    <DashboardLayout>
      {() => (
        <div className="min-h-full bg-gray-50">
          {/* Header azul oscuro */}
          <div className="bg-blue-900 text-white py-6">
            <div className="max-w-4xl mx-auto px-6 text-center">
              <h1 className="text-xl font-semibold">Comparación de pensum</h1>
            </div>
          </div>

          {/* Header azul claro */}
          <div className="bg-blue-400 text-white py-4">
            <div className="max-w-4xl mx-auto px-6 text-center">
              <h2 className="text-lg font-semibold">Comparación Pensum</h2>
              <h3 className="text-base">{estudiante.nombre}</h3>
            </div>
          </div>

          {/* Contenido principal */}
          <div className="max-w-4xl mx-auto p-6">
            {/* Info del estudiante */}
            <div className="bg-gray-100 rounded-lg p-4 mb-6">
              <div className="text-sm">
                <span className="font-semibold">Estudiante:</span> {estudiante.nombre} - 
                <span className="font-semibold"> ID:</span> {estudiante.id}
              </div>
              <div className="text-sm">
                <span className="font-semibold">Programa:</span> {estudiante.programa}
              </div>
            </div>

            {/* Leyenda */}
            <div className="bg-white rounded-lg border p-4 mb-6">
              <div className="flex flex-wrap gap-6 justify-center text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span>Aprobada</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <span>No aprobada</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-gray-400 rounded-full"></div>
                  <span>No cursada</span>
                </div>
              </div>
            </div>

            {/* Lista de materias */}
            <div className="bg-white rounded-lg border p-6 mb-6">
              <h3 className="text-lg font-semibold text-blue-900 mb-4">Materias Obligatorias:</h3>
              
              <div className="space-y-2">
                {estudiante.materias.map((materia) => (
                  <div
                    key={materia.id}
                    className={`flex items-center justify-between p-3 rounded-lg border ${
                      materia.estado === 'APROBADA' 
                        ? 'border-green-200 bg-green-50' 
                        : materia.estado === 'NO_APROBADA'
                        ? 'border-red-200 bg-red-50'
                        : 'border-gray-200 bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${
                        materia.estado === 'APROBADA' 
                          ? 'bg-green-500' 
                          : materia.estado === 'NO_APROBADA'
                          ? 'bg-red-500'
                          : 'bg-gray-400'
                      }`}></div>
                      <span className="font-medium">{materia.nombre}</span>
                    </div>
                    
                    <div className={`text-sm font-medium ${
                      materia.estado === 'APROBADA' 
                        ? 'text-green-600' 
                        : materia.estado === 'NO_APROBADA'
                        ? 'text-red-600'
                        : 'text-gray-500'
                    }`}>
                      {materia.estado === 'NO_CURSADA' 
                        ? 'No cursada'
                        : materia.estado === 'APROBADA'
                        ? `✓ ${materia.nota}`
                        : `✗ ${materia.nota}`
                      }
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Resumen */}
            <div className="bg-gray-100 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-blue-900 mb-2">Resumen:</h3>
              <div className="space-y-1 text-sm">
                <div className="text-green-600">
                  ✓ Aprobadas: {materiasAprobadas} materias
                </div>
                <div className="text-red-600">
                  ✗ No aprobadas: {materiasNoAprobadas} materias
                </div>
                <div className="text-gray-500">
                  ○ No cursadas: {materiasNoCursadas} materia{materiasNoCursadas !== 1 ? 's' : ''}
                </div>
              </div>
            </div>

            {/* Resultado final */}
            <div className={`rounded-lg p-4 mb-6 text-center font-semibold text-white ${
              estudiante.estado === 'APTO' ? 'bg-green-600' : 'bg-red-600'
            }`}>
              <div className="text-sm uppercase tracking-wide">RESULTADO:</div>
              <div className="text-lg">
                El estudiante {estudiante.estado === 'APTO' ? 'SÍ es apto' : 'NO es apto'}
              </div>
            </div>

            {/* Botones de acción */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={handleVolver}
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
      )}
    </DashboardLayout>
  );
}