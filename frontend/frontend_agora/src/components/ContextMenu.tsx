import React from 'react';
import { Edit2, Trash2 } from 'lucide-react';

interface Props {
  x: number;
  y: number;
  onEdit: () => void;
  onDelete: () => void;
  onClose: () => void;
}

export default function ContextMenu({ x, y, onEdit, onDelete, onClose }: Props) {
  return (
    <>
      {/* Overlay para cerrar el menú */}
      <div className="fixed inset-0 z-40" onClick={onClose} />
      
      {/* Menú contextual */}
      <div
        className="fixed z-50 bg-white rounded-lg shadow-lg border py-2 min-w-[120px]"
        style={{ left: x, top: y }}
      >
        <button
          onClick={() => { onEdit(); onClose(); }}
          className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-2 text-sm"
        >
          <Edit2 size={16} className="text-blue-600" />
          Editar
        </button>
        <button
          onClick={() => { onDelete(); onClose(); }}
          className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-2 text-sm"
        >
          <Trash2 size={16} className="text-red-600" />
          Eliminar
        </button>
      </div>
    </>
  );
}