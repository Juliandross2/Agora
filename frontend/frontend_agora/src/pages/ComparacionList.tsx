import React, { useState } from 'react';
import { Search, Download, Plus, FileSpreadsheet } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../DashboardLayout';
import { exportResumenToPDF, exportResumenToExcel } from '../utils/exportUtils';

interface Estudiante {
  id: string;
  nombre: string;
  programa: string;
  estado: 'APTO' | 'NO_APTO';
  porcentaje: number;
  iniciales: string;
}

export default function ComparacionList() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [filtroEstado, setFiltroEstado] = useState<'TODOS' | 'APTO' | 'NO_APTO'>('TODOS');
  
  // Variable debug para mostrar datos de ejemplo
  const DEBUG_MODE = true;

  // Datos de ejemplo para la demostración
  const estudiantesDemo: Estudiante[] = [
    {
      id: '12345',
      nombre: 'Juan Pérez',
      programa: 'Ing. Sistemas',
      estado: 'NO_APTO',
      porcentaje: 50,
      iniciales: 'JP'
    },
    {
      id: '12346',
      nombre: 'María González',
      programa: 'Ing. Sistemas',
      estado: 'APTO',
      porcentaje: 100,
      iniciales: 'MG'
    },
    {
      id: '12347',
      nombre: 'Carlos Rodríguez',
      programa: 'Ing. Sistemas',
      estado: 'NO_APTO',
      porcentaje: 75,
      iniciales: 'CR'
    }
  ];

  const estudiantes = DEBUG_MODE ? estudiantesDemo : [];

  // Filtrar estudiantes
  const estudiantesFiltrados = estudiantes.filter(estudiante => {
    const matchesSearch = estudiante.nombre.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesEstado = filtroEstado === 'TODOS' || estudiante.estado === filtroEstado;
    return matchesSearch && matchesEstado;
  });

  // Calcular estadísticas
  const totalEstudiantes = estudiantes.length;
  const aptos = estudiantes.filter(e => e.estado === 'APTO').length;
  const noAptos = estudiantes.filter(e => e.estado === 'NO_APTO').length;
  const porcentajeAptos = totalEstudiantes > 0 ? ((aptos / totalEstudiantes) * 100).toFixed(1) : '0';
  const porcentajeNoAptos = totalEstudiantes > 0 ? ((noAptos / totalEstudiantes) * 100).toFixed(1) : '0';

  const handleVerDetalle = (estudiante: Estudiante) => {
    // Navegar al detalle del estudiante
    navigate(`/comparacion-detalle/${estudiante.id}`);
  };

  const handleNuevaComparacion = () => {
    // Navegar a la página de comparación
    navigate('/comparacion');
  };

  const handleExportarPDF = async () => {
    try {
      exportResumenToPDF(estudiantes);
    } catch (error) {
      console.error('Error al exportar PDF:', error);
      alert('Error al generar el reporte PDF');
    }
  };

  const handleExportarExcel = async () => {
    try {
      exportResumenToExcel(estudiantes);
    } catch (error) {
      console.error('Error al exportar Excel:', error);
      alert('Error al generar el reporte Excel');
    }
  };

  if (!DEBUG_MODE && estudiantes.length === 0) {
    return (
      <DashboardLayout>
        {() => (
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
                onClick={handleNuevaComparacion}
                className="bg-blue-900 text-white px-6 py-3 rounded-md hover:bg-blue-800 transition flex items-center gap-2 mx-auto"
              >
                <Plus className="w-4 h-4" />
                Nueva Comparación
              </button>
            </div>
          </div>
        )}
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      {() => (
        <div className="min-h-full bg-gray-50">
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
                {estudiantesFiltrados.map((estudiante) => (
                  <div
                    key={estudiante.id}
                    className={`flex items-center justify-between p-4 rounded-lg border transition hover:shadow-sm ${
                      estudiante.estado === 'APTO' ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
                    }`}
                  >
                    <div className="flex items-center gap-4">
                      {/* Avatar */}
                      <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-white ${
                        estudiante.estado === 'APTO' ? 'bg-green-600' : 'bg-red-600'
                      }`}>
                        {estudiante.iniciales}
                      </div>
                      
                      {/* Info del estudiante */}
                      <div>
                        <div className="font-medium text-gray-900">{estudiante.nombre}</div>
                        <div className="text-sm text-gray-500">ID: {estudiante.id} - {estudiante.programa}</div>
                        <div className={`text-sm font-medium ${
                          estudiante.estado === 'APTO' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {estudiante.estado === 'APTO' 
                            ? `APTO (${estudiante.porcentaje}% completado)`
                            : `NO APTO (${estudiante.porcentaje}% completado)`
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
                ))}
              </div>
            </div>

            {/* Resumen General */}
            <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
              <h2 className="text-lg font-semibold text-blue-900 mb-4">Resumen General</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Total evaluados: </span>
                  <span className="font-semibold">{totalEstudiantes} estudiantes</span>
                </div>
                <div>
                  <span className="text-gray-600">Aptos: </span>
                  <span className="font-semibold text-green-600">{aptos} ({porcentajeAptos}%)</span>
                </div>
                <div>
                  <span className="text-gray-600">No aptos: </span>
                  <span className="font-semibold text-red-600">{noAptos} ({porcentajeNoAptos}%)</span>
                </div>
              </div>
            </div>

            {/* Botones de acción actualizados */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
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
                onClick={handleNuevaComparacion}
                className="flex items-center justify-center gap-2 px-8 py-3 bg-blue-900 text-white rounded-md hover:bg-blue-800 transition"
              >
                <Plus className="w-4 h-4" />
                Nueva Comparación
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}