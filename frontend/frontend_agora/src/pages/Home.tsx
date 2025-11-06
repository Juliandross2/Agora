import React, { useEffect, useState, useMemo, useRef } from 'react';
import { useActiveSection } from '../DashboardLayout';
import { useNavigate } from 'react-router-dom';
import { listarProgramas } from '../services/consumers/ProgramaClient';
import { obtenerPensumActual, obtenerEstadisticasPensum } from '../services/consumers/PensumClient';
import type { Programa } from '../services/domain/ProgramaModels';
import type { PensumEstadisticas } from '../services/domain/PensumModels';

export default function AgoraDashboard() {
  const { setActiveSection } = useActiveSection();
  const navigate = useNavigate();
  useEffect(() => { setActiveSection('home'); }, [setActiveSection]);

  const [programs, setPrograms] = useState<Programa[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const PAGE_SIZE = 5;

  // pensum stats cache: programId -> PensumEstadisticas | null (null = no pensum activo)
  const [pensumStats, setPensumStats] = useState<Record<number, PensumEstadisticas | null>>({});
  const [loadingPensum, setLoadingPensum] = useState<Record<number, boolean>>({});

  // refs para controlar solicitudes ya hechas / en progreso
  const fetchedRef = useRef<Set<number>>(new Set());
  const fetchingRef = useRef<Set<number>>(new Set());

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await listarProgramas();
        if (!mounted) return;
        setPrograms(Array.isArray(res.programas) ? res.programas : []);
        setCurrentPage(1);
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

  // Fetch pensum actual + estadisticas for visible programs (cached)
  useEffect(() => {
    let mounted = true;

    displayedPrograms.forEach((program) => {
      const pid = program.programa_id;

      // si ya se obtuvo o ya está en curso, saltar
      if (fetchedRef.current.has(pid) || fetchingRef.current.has(pid)) return;

      fetchingRef.current.add(pid);
      setLoadingPensum((s) => ({ ...s, [pid]: true }));

      (async () => {
        try {
          // obtenerPensumActual devuelve pensum_actual = null si no hay pensum (no lanza)
          const res = await obtenerPensumActual(pid).catch(() => null as any);

          if (!mounted) return;

          if (!res || !res.pensum_actual) {
            // no hay pensum activo
            setPensumStats((s) => ({ ...s, [pid]: null }));
          } else {
            try {
              const stats = await obtenerEstadisticasPensum(res.pensum_actual.pensum_id);
              if (!mounted) return;
              setPensumStats((s) => ({ ...s, [pid]: stats }));
            } catch (err) {
              // fallo al obtener estadísticas: marcar como no disponible
              setPensumStats((s) => ({ ...s, [pid]: null }));
            }
          }
        } catch (err) {
          // cualquier otro error -> marcar como no disponible
          setPensumStats((s) => ({ ...s, [pid]: null }));
        } finally {
          fetchingRef.current.delete(pid);
          fetchedRef.current.add(pid);
          if (mounted) setLoadingPensum((s) => ({ ...s, [pid]: false }));
        }
      })();
    });

    return () => { mounted = false; };
  }, [displayedPrograms]);

  return (
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
          {loading && <div className="text-center text-gray-600">Cargando programas...</div>}
          {error && <div className="text-center text-red-600">{error}</div>}
          {!loading && !error && programs.length === 0 && <div className="text-center text-gray-600">No hay programas disponibles.</div>}

          {!loading && !error && programs.length > 0 && (
            <>
              <div className="space-y-4">
                {displayedPrograms.map((program) => {
                  const stats = pensumStats[program.programa_id];
                  const isLoadingPensum = !!loadingPensum[program.programa_id];

                  return (
                    <div
                      key={program.programa_id}
                      role="button"
                      tabIndex={0}
                      onClick={() => navigate(`/pensum/${program.programa_id}`)}
                      onKeyDown={(e) => { if (e.key === 'Enter') navigate(`/pensum/${program.programa_id}`); }}
                      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition cursor-pointer"
                    >
                      <div className="flex items-center gap-6">
                        <div className="w-16 h-16 bg-blue-900 rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">
                          {String(program.nombre_programa).slice(0,2).toUpperCase()}
                        </div>
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-800 mb-1">{program.nombre_programa}</h3>

                          {isLoadingPensum && <p className="text-sm text-gray-500">Cargando pensum...</p>}

                          {!isLoadingPensum && stats && (
                            <p className="text-sm text-gray-600">
                              Pensum {stats.anio_creacion} • {stats.creditos_obligatorios_totales} créditos obligatorios • {stats.total_materias} materias
                            </p>
                          )}

                          {!isLoadingPensum && stats === null && (
                            <div className="flex items-center gap-3">
                              <p className="text-sm text-red-600">No tiene pensum activo</p>
                              <button
                                onClick={(e) => { e.stopPropagation(); navigate('/gestion-programas'); }}
                                className="px-3 py-1 bg-green-600 text-white rounded-md text-sm hover:bg-green-700 transition"
                              >
                                Añadir pensum
                              </button>
                            </div>
                          )}

                          {!isLoadingPensum && stats === undefined && (
                            <p className="text-sm text-gray-500">Sin información de pensum</p>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="mt-6 flex items-center justify-between">
                <div className="text-sm text-gray-600">Página {currentPage} de {totalPages}</div>

                <div className="flex items-center gap-2">
                  <button onClick={() => goToPage(currentPage - 1)} disabled={currentPage === 1} className="px-3 py-1 rounded-md border hover:bg-gray-100 disabled:opacity-50">Anterior</button>

                  <div className="flex items-center gap-1">
                    {Array.from({ length: totalPages }, (_, i) => i + 1)
                      .filter((p) => {
                        if (totalPages <= 5) return true;
                        if (currentPage <= 3) return p <= 5;
                        if (currentPage >= totalPages - 3) return p > totalPages - 5;
                        return Math.abs(p - currentPage) <= 3;
                      })
                      .map((p) => (
                        <button key={p} onClick={() => goToPage(p)} className={`px-3 py-1 rounded-md ${p === currentPage ? 'bg-blue-900 text-white' : 'hover:bg-gray-100'}`}>{p}</button>
                      ))}
                  </div>

                  <button onClick={() => goToPage(currentPage + 1)} disabled={currentPage === totalPages} className="px-3 py-1 rounded-md border hover:bg-gray-100 disabled:opacity-50">Siguiente</button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
}