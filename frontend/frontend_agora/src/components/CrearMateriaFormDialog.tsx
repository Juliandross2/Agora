import React, { useState, useEffect } from 'react';
import { useSnackbar } from 'notistack';
import { crearMateria } from '../services/consumers/MateriaClient';
import type { MateriaCreatePayload } from '../services/consumers/MateriaClient';
import type { Materia as MateriaModel } from '../services/domain/PensumModels';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  pensumId: number | null;
  onCreated?: (materia?: MateriaModel) => void;
}

export default function CrearMateriaFormDialog({ isOpen, onClose, pensumId, onCreated }: Props) {
  const { enqueueSnackbar } = useSnackbar();
  const [nombre, setNombre] = useState('');
  const [creditos, setCreditos] = useState<number>(3);
  const [semestre, setSemestre] = useState<number>(1);
  const [esObligatoria, setEsObligatoria] = useState(true);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      // reset form when closing
      setNombre('');
      setCreditos(3);
      setSemestre(1);
      setEsObligatoria(true);
      setLoading(false);
    }
  }, [isOpen]);

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!pensumId) {
      enqueueSnackbar('No hay pensum seleccionado', { variant: 'error' });
      return;
    }
    setLoading(true);
    const payload: MateriaCreatePayload = {
      pensum_id: pensumId,
      nombre_materia: nombre.trim(),
      creditos,
      semestre,
      es_obligatoria: esObligatoria,
      es_activa: true,
    };

    try {
      const res = await crearMateria(payload);
      enqueueSnackbar(res.message || 'Materia creada correctamente', { variant: 'success' });
      onCreated?.(res.materia as MateriaModel);
      onClose();
    } catch (err: any) {
      const msg = err?.message || 'Error al crear materia';
      enqueueSnackbar(msg, { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Crear Materia</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-700 mb-1">Nombre</label>
            <input
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
              className="w-full px-3 py-2 border rounded"
              placeholder="Programación I"
            />
          </div>

          <div className="flex gap-3">
            <div className="flex-1">
              <label className="block text-sm text-gray-700 mb-1">Créditos</label>
              <input
                type="number"
                value={creditos}
                min={1}
                onChange={(e) => setCreditos(Number(e.target.value))}
                required
                className="w-full px-3 py-2 border rounded"
              />
            </div>
            <div style={{ width: 110 }}>
              <label className="block text-sm text-gray-700 mb-1">Semestre</label>
              <input
                type="number"
                value={semestre}
                min={1}
                max={10}
                onChange={(e) => setSemestre(Number(e.target.value))}
                required
                className="w-full px-3 py-2 border rounded"
              />
            </div>
          </div>

          <div className="flex items-center gap-3">
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={esObligatoria}
                onChange={(e) => setEsObligatoria(e.target.checked)}
              />
              Obligatoria
            </label>
          </div>

          <div className="flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border rounded text-sm"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-900 text-white rounded text-sm"
              disabled={loading}
            >
              {loading ? 'Creando...' : 'Crear materia'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}