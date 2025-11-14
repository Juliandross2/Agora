import React, { useEffect, useState } from 'react';
import { X, BookOpen } from 'lucide-react';
import { obtenerPrograma } from '../services/consumers/ProgramaClient';
import type { Programa } from '../services/domain/ProgramaModels';

interface ProgramaDetailDialogProps {
  isOpen: boolean;
  onClose: () => void;
  programaId: number | null;
}

const ProgramaDetailDialog: React.FC<ProgramaDetailDialogProps> = ({
  isOpen,
  onClose,
  programaId
}) => {
  const [programa, setPrograma] = useState<Programa | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen && programaId) {
      loadPrograma();
    }
  }, [isOpen, programaId]);

  const loadPrograma = async () => {
    if (!programaId) return;

    setLoading(true);
    setError(null);
    try {
      const res = await obtenerPrograma(programaId);
      setPrograma(res.programa);
    } catch (err: any) {
      setError(err?.message || 'Error al cargar el programa');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-800">Detalles del Programa</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition"
          >
            <X size={24} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {loading && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-900"></div>
              <p className="mt-4 text-gray-600">Cargando información...</p>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {!loading && !error && programa && (
            <div className="space-y-6">
              <div className="bg-gradient-to-r from-blue-900 to-blue-800 rounded-xl p-6 text-white">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
                    <BookOpen size={32} />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold">{programa.nombre_programa}</h3>
                    <p className="text-blue-100 mt-1">
                      Estado: {programa.es_activo ? 'Activo' : 'Inactivo'}
                    </p>
                  </div>
                </div>
              </div>

              <div className="border border-gray-200 rounded-xl p-6">
                <h4 className="text-lg font-semibold text-gray-800 mb-4">Información General</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">ID del Programa</p>
                    <p className="font-medium text-gray-900">{programa.programa_id}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Estado</p>
                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                      programa.es_activo 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {programa.es_activo ? 'Activo' : 'Inactivo'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="border border-gray-200 rounded-xl p-6">
                <h4 className="text-lg font-semibold text-gray-800 mb-4">Pensum Asociado</h4>
                <div className="text-center py-8 text-gray-500">
                  <BookOpen size={48} className="mx-auto mb-3 text-gray-300" />
                  <p>No hay información de pensum disponible</p>
                  <p className="text-sm mt-2">Esta funcionalidad estará disponible próximamente</p>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="border-t border-gray-200 p-6">
          <button
            onClick={onClose}
            className="w-full px-4 py-2 bg-blue-900 text-white rounded-lg hover:bg-blue-800 transition"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProgramaDetailDialog;