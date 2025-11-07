import React, { useEffect, useState, useMemo } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useSnackbar } from 'notistack';
import { Edit2, Trash2, Plus } from 'lucide-react';
import {
  listarElectivasActivas,
  crearElectiva,
  actualizarElectiva,
  eliminarElectiva
} from '../services/consumers/ElectivaClient';
import type { Electiva } from '../services/domain/ElectivaModels';
import ElectivaFormDialog from '../components/ElectivaFormDialog';
import ConfirmDialog from '../components/ConfirmDialog';

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

export default function GestionElectivas() {
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const query = useQuery();
  const programaIdParam = query.get('programaId');
  const programaId = programaIdParam ? parseInt(programaIdParam, 10) : null;

  const [electivas, setElectivas] = useState<Electiva[]>([]);
  const [loading, setLoading] = useState(false);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selected, setSelected] = useState<Electiva | null>(null);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [toDelete, setToDelete] = useState<Electiva | null>(null);

  const PAGE_SIZE = 8;
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = useMemo(() => Math.max(1, Math.ceil(electivas.length / PAGE_SIZE)), [electivas.length]);
  const displayed = useMemo(() => {
    const start = (currentPage - 1) * PAGE_SIZE;
    return electivas.slice(start, start + PAGE_SIZE);
  }, [electivas, currentPage]);

  const load = async () => {
    setLoading(true);
    try {
      const res = await listarElectivasActivas();
      const list = Array.isArray(res.electivas) ? res.electivas : [];
      setElectivas(programaId ? list.filter((e) => e.programa_id === programaId) : list);
      enqueueSnackbar('Electivas cargadas', { variant: 'success' });
    } catch (err: any) {
      const msg = err?.message || 'Error al cargar electivas';
      enqueueSnackbar(msg, { variant: 'error' });
      setElectivas([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // reset pagination when programaId changes
    setCurrentPage(1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [programaId]);

  const openCreate = () => {
    setSelected(null);
    setIsFormOpen(true);
  };

  const openEdit = (e: Electiva) => {
    setSelected(e);
    setIsFormOpen(true);
  };

  const handleSaved = async (saved?: Electiva) => {
    // recargar lista y notificar
    await load();
    if (saved) {
      enqueueSnackbar(saved ? 'Guardado correctamente' : 'Operación completada', { variant: 'success' });
    }
  };

  const handleDeleteClick = (e: Electiva) => {
    setToDelete(e);
    setIsDeleteOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!toDelete) return;
    try {
      await eliminarElectiva(toDelete.electiva_id);
      enqueueSnackbar('Electiva eliminada', { variant: 'success' });
      await load();
    } catch (err: any) {
      const msg = err?.message || 'Error al eliminar electiva';
      enqueueSnackbar(msg, { variant: 'error' });
    } finally {
      setIsDeleteOpen(false);
      setToDelete(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200 px-8 py-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate(-1)} className="text-blue-900 hover:text-blue-700 transition">
            ← Volver
          </button>
          <h1 className="text-2xl font-bold text-blue-900">Gestión de Electivas {programaId ? `• Programa ${programaId}` : ''}</h1>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={openCreate}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium flex items-center gap-2"
          >
            <Plus size={16} /> Añadir
          </button>
        </div>
      </div>

      <div className="p-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Nombre</th>
                <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">Estado</th>
                <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {loading && (
                <tr>
                  <td colSpan={4} className="px-6 py-12 text-center text-gray-600">Cargando electivas...</td>
                </tr>
              )}

              {!loading && displayed.length === 0 && (
                <tr>
                  <td colSpan={4} className="px-6 py-12 text-center text-gray-600">No se encontraron electivas</td>
                </tr>
              )}

              {!loading && displayed.map((e) => (
                <tr key={e.electiva_id} className="border-b border-gray-100 hover:bg-gray-50 transition">
                  <td className="px-6 py-4">
                    <div className="font-medium text-gray-900">{e.nombre_electiva}</div>
                  </td>
                  <td className="px-6 py-4 text-center">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${e.es_activa ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-700'}`}>
                      {e.es_activa ? 'Activa' : 'Inactiva'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    <div className="flex items-center justify-center gap-2">
                      <button
                        onClick={() => openEdit(e)}
                        className="w-10 h-10 bg-blue-900 text-white rounded-full flex items-center justify-center hover:bg-blue-800 transition"
                        title="Editar"
                      >
                        <Edit2 size={16} />
                      </button>
                      <button
                        onClick={() => handleDeleteClick(e)}
                        className="w-10 h-10 bg-red-600 text-white rounded-full flex items-center justify-center hover:bg-red-700 transition"
                        title="Eliminar"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {electivas.length > PAGE_SIZE && (
          <div className="mt-6 flex items-center justify-center gap-2">
            <button
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="px-3 py-2 border rounded disabled:opacity-50"
            >
              ←
            </button>
            <div className="flex items-center gap-1">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
                <button
                  key={p}
                  onClick={() => setCurrentPage(p)}
                  className={`w-9 h-9 rounded-lg font-medium ${p === currentPage ? 'bg-blue-900 text-white' : 'hover:bg-gray-100'}`}
                >
                  {p}
                </button>
              ))}
            </div>
            <button
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="px-3 py-2 border rounded disabled:opacity-50"
            >
              →
            </button>
          </div>
        )}
      </div>

      <ElectivaFormDialog
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        electiva={selected}
        defaultProgramaId={programaId}
        onSaved={handleSaved}
      />

      <ConfirmDialog
        isOpen={isDeleteOpen}
        onCancel={() => setIsDeleteOpen(false)}
        onConfirm={handleDeleteConfirm}
        title="Eliminar Electiva"
        description={`¿Está seguro de marcar como inactiva la electiva "${toDelete?.nombre_electiva}"?`}
        confirmLabel="Eliminar"
        cancelLabel="Cancelar"
      />
    </div>
  );
}