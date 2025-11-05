import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../DashboardLayout';

export default function ComparacionPensum() {
  const [text, setText] = useState<string>('');
  const [files, setFiles] = useState<FileList | null>(null);
  const [evaluating, setEvaluating] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files;
    setFiles(f);
    if (!f) return;
    const names = Array.from(f).map((x) => x.name).join('\n');
    setText((prev) => (prev ? prev + '\n' + names : names));
  };

  const handleEvaluate = async () => {
    setEvaluating(true);
    try {
      // Simulación del proceso de evaluación
      await new Promise((r) => setTimeout(r, 2000));
      
      // Redirigir a la página de resultados
      navigate('/comparacion-resultados');
    } finally {
      setEvaluating(false);
    }
  };

  const handleClear = () => {
    setText('');
    setFiles(null);
  };

  return (
    <DashboardLayout>
      {() => (
        <div className="min-h-full min-w-full">
          {/* Top blue header */}
          <div className="bg-blue-900 text-white py-6">
            <div className="max-w-4xl mx-auto text-center">
              <h2 className="text-lg font-semibold">Comparación de pensum</h2>
            </div>
          </div>

          {/* Main centered card */}
          <div className="max-w-3xl mx-auto p-8">
            <div className="bg-white rounded-xl shadow-sm border p-6">
              <h3 className="text-center text-blue-900 font-semibold mb-4">Ingrese las historias academicas de los Estudiantes</h3>
              <p className="text-center text-sm text-gray-500 mb-4">En formato .CSV</p>

              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Ingrese más historias academicas aquí"
                className="w-full h-48 border rounded p-3 text-sm resize-none mb-4"
              />

              <div className="flex items-center gap-3">
                <label className="flex items-center gap-2 bg-gray-100 px-3 py-2 rounded cursor-pointer hover:bg-gray-200">
                  <input type="file" accept=".csv" multiple onChange={handleFileChange} className="hidden" />
                  <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M7 16v4h10v-4M12 12v8M12 12V4m0 8l4-4m-4 4L8 8"/></svg>
                  <span className="text-sm text-gray-700">Cargar desde archivo (.csv)</span>
                </label>

                <button
                  onClick={handleEvaluate}
                  disabled={evaluating}
                  className="ml-2 px-4 py-2 bg-blue-900 text-white rounded hover:bg-blue-800 disabled:opacity-60"
                >
                  {evaluating ? 'Evaluando...' : 'Evaluar Estudiantes'}
                </button>

                <button
                  onClick={handleClear}
                  className="ml-auto px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
                >
                  Limpiar Todo
                </button>
              </div>

              <div className="mt-4 text-center text-sm text-blue-700 bg-blue-50 p-3 rounded">
                El proceso evaluará automáticamente el pensum vs historia académica de cada estudiante
              </div>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}