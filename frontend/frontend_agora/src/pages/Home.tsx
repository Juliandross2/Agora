import React, { useEffect, useState, useMemo } from 'react';
import DashboardLayout from '../DashboardLayout';
import { listarProgramas } from '../services/consumers/ProgramaClient';
import type { Programa } from '../services/domain/ProgramaModels';

export default function AgoraDashboard() {
  const [programs, setPrograms] = useState<Programa[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const PAGE_SIZE = 5; 

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await listarProgramas();
        if (!mounted) return;
        setPrograms(Array.isArray(res.programas) ? res.programas : []);
        setCurrentPage(1); // reset pagina al recargar datos
      } catch (err: any) {
        if (!mounted) return;
        setError(err?.message || 'Error al cargar programas');
      } finally {
        if (mounted) setLoading(false);
      }
    };
    load();
    return () => { mounted = false; };
  }, []);

  const totalPages = Math.max(1, Math.ceil(programs.length / PAGE_SIZE));

  const displayedPrograms = useMemo(() => {
    const start = (currentPage - 1) * PAGE_SIZE;
    return programs.slice(start, start + PAGE_SIZE);
  }, [programs, currentPage]);

  const goToPage = (p: number) => {
    const page = Math.min(Math.max(1, p), totalPages);
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <DashboardLayout>
      {(activeSection) => (
        <>
          {/* Top Bar */}
          <div className="bg-white border-b border-gray-200 px-8 py-2 flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-800">Home</h1>
            <button className="w-8 h-8 bg-blue-900 rounded-full flex items-center justify-center text-white hover:bg-blue-800 transition">
              <span className="text-xl">!</span>
            </button>
          </div>

          {/* Right content area */}
          <div className="p-8">
            {activeSection === 'home' && (
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

                {/* lista con altura controlada + paginación */}
                <div className="space-y-4">
                  {loading && (
                    <div className="text-center text-gray-600">Cargando programas...</div>
                  )}

                  {error && (
                    <div className="text-center text-red-600">{error}</div>
                  )}

                  {!loading && !error && programs.length === 0 && (
                    <div className="text-center text-gray-600">No hay programas disponibles.</div>
                  )}

                  {!loading && !error && (
                    <>
                      <div className="space-y-4">
                        {displayedPrograms.map((program) => (
                          <div key={program.programa_id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition">
                            <div className="flex items-center gap-6">
                              <div className="w-16 h-16 bg-blue-900 rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">
                                {String(program.nombre_programa).slice(0,2).toUpperCase()}
                              </div>
                              <div className="flex-1">
                                <h3 className="text-lg font-semibold text-gray-800 mb-1">{program.nombre_programa}</h3>
                                {/* Por ahora los créditos se muestran como 0; dejar preparado para cuando el backend los entregue */}
                                <p className="text-gray-600">0 Créditos Totales</p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>

                      {/* pagination controls */}
                      <div className="mt-6 flex items-center justify-between">
                        <div className="text-sm text-gray-600">
                          Página {currentPage} de {totalPages}
                        </div>

                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => goToPage(currentPage - 1)}
                            disabled={currentPage === 1}
                            className="px-3 py-1 rounded-md border hover:bg-gray-100 disabled:opacity-50"
                          >
                            Anterior
                          </button>

                          {/* mostrar algunos números de página (máx 5) */}
                          <div className="flex items-center gap-1">
                            {Array.from({ length: totalPages }, (_, i) => i + 1)
                              .filter((p) => {
                                if (totalPages <= 5) return true;
                                if (currentPage <= 3) return p <= 5;
                                if (currentPage >= totalPages - 3) return p > totalPages - 5;
                                return Math.abs(p - currentPage) <= 3;
                              })
                              .map((p) => (
                                <button
                                  key={p}
                                  onClick={() => goToPage(p)}
                                  className={`px-3 py-1 rounded-md ${p === currentPage ? 'bg-blue-900 text-white' : 'hover:bg-gray-100'}`}
                                >
                                  {p}
                                </button>
                              ))}
                          </div>

                          <button
                            onClick={() => goToPage(currentPage + 1)}
                            disabled={currentPage === totalPages}
                            className="px-3 py-1 rounded-md border hover:bg-gray-100 disabled:opacity-50"
                          >
                            Siguiente
                          </button>
                        </div>
                      </div>
                    </>
                  )}
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