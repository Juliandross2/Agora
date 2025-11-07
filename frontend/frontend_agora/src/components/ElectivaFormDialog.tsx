import React, { useEffect, useState } from 'react';
import type { Electiva, ElectivaCreatePayload, ElectivaUpdatePayload } from '../services/domain/ElectivaModels';
import { crearElectiva, actualizarElectiva } from '../services/consumers/ElectivaClient';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSaved?: (electiva?: Electiva) => void;
  electiva?: Electiva | null;
  defaultProgramaId?: number | null;
}

export default function ElectivaFormDialog({ isOpen, onClose, onSaved, electiva, defaultProgramaId }: Props) {
  const [nombre, setNombre] = useState('');
  const [esActiva, setEsActiva] = useState(true);
  const [programaId, setProgramaId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && electiva) {
      setNombre(electiva.nombre_electiva ?? '');
      setEsActiva(typeof electiva.es_activa === 'boolean' ? electiva.es_activa : true);
      setProgramaId(electiva.programa_id ?? defaultProgramaId ?? null);
    } else if (isOpen) {
      setNombre('');
      setEsActiva(true);
      setProgramaId(defaultProgramaId ?? null);
    } else {
      setLoading(false);
    }
  }, [isOpen, electiva, defaultProgramaId]);

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    setLoading(true);
    try {
      if (!programaId) throw new Error('programa_id requerido');
      if (electiva && electiva.electiva_id) {
        const payload: ElectivaUpdatePayload = { nombre_electiva: nombre.trim(), es_activa: esActiva };
        const res = await actualizarElectiva(electiva.electiva_id, payload);
        onSaved?.(res.electiva);
      } else {
        const payload: ElectivaCreatePayload = { programa_id: programaId, nombre_electiva: nombre.trim(), es_activa: esActiva };
        const res = await crearElectiva(payload);
        onSaved?.(res.electiva);
      }
      onClose();
    } catch (err: any) {
      onSaved?.();
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">{electiva ? 'Editar electiva' : 'Crear electiva'}</h3>
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
              placeholder="Tópicos en IA"
            />
          </div>

          <div className="flex items-center gap-3">
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={esActiva}
                onChange={(e) => setEsActiva(e.target.checked)}
              />
              Activa
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
              disabled={loading || !programaId}
            >
              {loading ? 'Guardando...' : electiva ? 'Actualizar' : 'Crear'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}