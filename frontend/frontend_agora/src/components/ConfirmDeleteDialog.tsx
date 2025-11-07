import React from 'react';

interface Props {
  isOpen: boolean;
  onCancel: () => void;
  onConfirm: () => void;
  loading?: boolean;
  materiaNombre?: string;
}

export default function ConfirmDeleteDialog({ 
  isOpen, 
  onCancel, 
  onConfirm, 
  loading = false,
  materiaNombre = ''
}: Props) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
        <h3 className="text-lg font-semibold mb-4">Eliminar Materia</h3>
        <p className="text-gray-600 mb-6">
          ¿Está seguro de eliminar la materia "{materiaNombre}"? Esta acción no se puede deshacer.
        </p>
        <div className="flex items-center justify-end gap-3">
          <button
            onClick={onCancel}
            disabled={loading}
            className="px-4 py-2 border rounded text-sm"
          >
            Cancelar
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className="px-4 py-2 bg-red-600 text-white rounded text-sm hover:bg-red-700"
          >
            {loading ? 'Eliminando...' : 'Eliminar'}
          </button>
        </div>
      </div>
    </div>
  );
}