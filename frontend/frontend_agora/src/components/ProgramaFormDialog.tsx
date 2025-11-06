import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import type { Programa } from '../services/domain/ProgramaModels';

interface ProgramaFormDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (programa: { nombre_programa: string; programa_id?: number }) => Promise<void>;
  programa?: Programa | null;
  mode: 'create' | 'edit';
}

const ProgramaFormDialog: React.FC<ProgramaFormDialogProps> = ({
  isOpen,
  onClose,
  onSubmit,
  programa,
  mode
}) => {
  const [formData, setFormData] = useState({
    nombre_programa: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (programa && mode === 'edit') {
      setFormData({
        nombre_programa: programa.nombre_programa
      });
    } else {
      setFormData({
        nombre_programa: ''
      });
    }
    setError(null);
  }, [programa, mode, isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (mode === 'edit' && programa) {
        await onSubmit({ ...formData, programa_id: programa.programa_id });
      } else {
        await onSubmit(formData);
      }
      onClose();
    } catch (err: any) {
      setError(err.message || 'Error al guardar el programa');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl max-w-md w-full">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-800">
            {mode === 'create' ? '+ Agregar Programa' : 'Editar Programa'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition"
            disabled={loading}
          >
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nombre del Programa *
            </label>
            <input
              type="text"
              value={formData.nombre_programa}
              onChange={(e) => setFormData({ ...formData, nombre_programa: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-900 focus:border-transparent"
              placeholder="Ej: Ingeniería de Sistemas"
              required
              disabled={loading}
              maxLength={100}
            />
            <p className="mt-1 text-xs text-gray-500">
              Máximo 100 caracteres
            </p>
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-blue-900 text-white rounded-lg hover:bg-blue-800 transition disabled:opacity-50"
              disabled={loading}
            >
              {loading ? 'Guardando...' : (mode === 'create' ? 'Crear' : 'Guardar')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProgramaFormDialog;