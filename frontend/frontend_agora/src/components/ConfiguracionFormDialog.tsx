import React, { useEffect, useState } from 'react';
import { useSnackbar } from 'notistack';
import type { Configuracion } from '../services/consumers/ConfiguracionClient';
import { crearConfiguracion, actualizarConfiguracion } from '../services/consumers/ConfiguracionClient';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSaved?: () => void;
  configuracion?: Configuracion | null;
  programaId: number;
  programaNombre: string;
}

export default function ConfiguracionFormDialog({
  isOpen,
  onClose,
  onSaved,
  configuracion,
  programaId,
  programaNombre,
}: Props) {
  const { enqueueSnackbar } = useSnackbar();
  const [notaAprobatoria, setNotaAprobatoria] = useState(3.0);
  const [semestreLimite, setSemestreLimite] = useState(7);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && configuracion) {
      setNotaAprobatoria(configuracion.nota_aprobatoria);
      setSemestreLimite(configuracion.semestre_limite_electivas);
    } else if (isOpen) {
      setNotaAprobatoria(3.0);
      setSemestreLimite(7);
    }
  }, [isOpen, configuracion]);

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    setLoading(true);
    try {
      if (configuracion) {
        // Actualizar configuración existente
        await actualizarConfiguracion(configuracion.configuracion_id, {
          nota_aprobatoria: notaAprobatoria,
          semestre_limite_electivas: semestreLimite,
        });
        enqueueSnackbar('Configuración actualizada correctamente', { variant: 'success' });
      } else {
        // Crear nueva configuración
        await crearConfiguracion({
          programa_id: programaId,
          nota_aprobatoria: notaAprobatoria,
          semestre_limite_electivas: semestreLimite,
        });
        enqueueSnackbar('Configuración creada correctamente', { variant: 'success' });
      }
      onSaved?.();
      onClose();
    } catch (err: any) {
      const msg = err?.message || 'Error al guardar configuración';
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
          <h3 className="text-lg font-semibold">
            {configuracion ? 'Editar configuración' : 'Crear configuración'}
          </h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">✕</button>
        </div>

        <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-sm text-blue-900">
            <strong>Programa:</strong> {programaNombre}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nota aprobatoria *
            </label>
            <input
              type="number"
              step="0.1"
              min="0"
              max="5"
              value={notaAprobatoria}
              onChange={(e) => setNotaAprobatoria(parseFloat(e.target.value))}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="3.0"
            />
            <p className="text-xs text-gray-500 mt-1">Rango: 0 - 5</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Semestre límite para electivas *
            </label>
            <input
              type="number"
              min="1"
              max="12"
              value={semestreLimite}
              onChange={(e) => setSemestreLimite(parseInt(e.target.value, 10))}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="7"
            />
            <p className="text-xs text-gray-500 mt-1">Semestre máximo en el que un estudiante puede cursar electivas</p>
          </div>

          <div className="bg-gray-50 p-3 rounded-lg border">
            <p className="text-xs text-gray-600">
              <strong>Resumen:</strong> Los estudiantes necesitan una nota mínima de <strong>{notaAprobatoria}</strong> y deben estar en semestre <strong>{semestreLimite}</strong> o anterior para acceder a electivas.
            </p>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-900 text-white rounded-lg text-sm font-medium hover:bg-blue-800 disabled:opacity-50"
              disabled={loading}
            >
              {loading ? 'Guardando...' : configuracion ? 'Actualizar' : 'Crear'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
