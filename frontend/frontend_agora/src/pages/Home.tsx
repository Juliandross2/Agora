import React from 'react';
import DashboardLayout from '../DashboardLayout';

export default function AgoraDashboard() {
  const programs = [
    { name: "Ingeniería de Sistemas", credits: 165 },
    { name: "Ingeniería electrónica y telecomunicaciones", credits: 160 },
    { name: "Ingeniería Civil", credits: 170 }
  ];

  return (
    <DashboardLayout>
      {(activeSection) => (
        <>
          {/* Top Bar */}
          <div className="bg-white border-b border-gray-200 px-8 py-6 flex items-center justify-between">
            <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
            <button className="w-12 h-12 bg-blue-900 rounded-full flex items-center justify-center text-white hover:bg-blue-800 transition">
              <span className="text-xl">!</span>
            </button>
          </div>

          {/* Right content area */}
          <div className="p-8">
            {activeSection === 'programas' && (
              <>
                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 mb-8 overflow-hidden">
                  <div className="bg-blue-900 text-white px-8 py-6">
                    <h2 className="text-2xl font-bold">Programas Activos</h2>
                  </div>
                  <div className="px-8 py-12">
                    <div className="text-6xl font-bold text-blue-900 text-center">
                      {programs.length}
                    </div>
                  </div>
                </div>

                <div className="mb-6">
                  <h2 className="text-2xl font-bold text-blue-900 mb-6">Programas</h2>
                </div>

                <div className="space-y-4">
                  {programs.map((program, index) => (
                    <div key={index} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition">
                      <div className="flex items-center gap-6">
                        <div className="w-16 h-16 bg-blue-900 rounded-full flex-shrink-0"></div>
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-800 mb-1">{program.name}</h3>
                          <p className="text-gray-600">{program.credits} Créditos Totales</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}

            {activeSection === 'comparacion' && (
              <div className="bg-white rounded-xl p-8 shadow-sm border">
                <h2 className="text-2xl font-bold mb-4">Comparación de pensum</h2>
                <p className="text-gray-600">Aquí va la interfaz para comparar pensums.</p>
              </div>
            )}

            {activeSection === 'configuracion' && (
              <div className="bg-white rounded-xl p-8 shadow-sm border">
                <h2 className="text-2xl font-bold mb-4">Configuración</h2>
                <p className="text-gray-600">Ajustes y opciones del sistema.</p>
              </div>
            )}
          </div>
        </>
      )}
    </DashboardLayout>
  );
}