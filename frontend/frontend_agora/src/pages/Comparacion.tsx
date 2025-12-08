import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSnackbar } from 'notistack';
import { Upload, X, AlertCircle } from 'lucide-react';
import { listarProgramas } from '../services/consumers/ProgramaClient';
import { obtenerPensumActual, obtenerMateriasPorSemestre } from '../services/consumers/PensumClient';
import { verificarElegibilidadMasiva } from '../services/consumers/ComparacionClient';
import type { Programa } from '../services/domain/ProgramaModels';
import type { VerificacionMasivaResponse } from '../services/consumers/ComparacionClient';
import { guardarResultadosComparacion, limpiarResultadosComparacion } from '../utils/storageUtils';
import { buildPensumMateriasResumen } from '../utils/pensumUtils';
import { obtenerConfiguracionActiva } from '../services/consumers/ConfiguracionClient';

const MAX_FILES = 50;

export default function ComparacionPensum() {
  const [files, setFiles] = useState<File[]>([]);
  const [programaId, setProgramaId] = useState<number | null>(null);
  const [programas, setProgramas] = useState<Programa[]>([]);
  const [loadingProgramas, setLoadingProgramas] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();

  const obtenerPensumMetadata = async (programa: number) => {
    try {
      const pensumActual = await obtenerPensumActual(programa);
      const pensumId = pensumActual.pensum_actual?.pensum_id ?? null;

      if (pensumId) {
        const materiasPorSemestre = await obtenerMateriasPorSemestre(pensumId);
        return {
          pensumId,
          pensumMaterias: buildPensumMateriasResumen(materiasPorSemestre),
        };
      }

      return { pensumId, pensumMaterias: [] };
    } catch (error) {
      console.warn('No fue posible obtener las materias del pensum', error);
      return { pensumId: null, pensumMaterias: [] };
    }
  };

  const obtenerConfiguracionMetadata = async (programa: number) => {
    try {
      const config = await obtenerConfiguracionActiva(programa);
      return { semestreLimite: config.semestre_limite_electivas };
    } catch (error) {
      console.warn('No fue posible obtener la configuración de elegibilidad', error);
      return { semestreLimite: null };
    }
  };

  useEffect(() => {
    // Limpiar resultados previos al entrar a esta vista
    limpiarResultadosComparacion();
    
    const load = async () => {
      setLoadingProgramas(true);
      try {
        const res = await listarProgramas();
        setProgramas(Array.isArray(res.programas) ? res.programas : []);
      } catch (err: any) {
        enqueueSnackbar(err?.message || 'Error al cargar programas', { variant: 'error' });
      } finally {
        setLoadingProgramas(false);
      }
    };
    load();
  }, [enqueueSnackbar]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newFiles = e.target.files;
    if (!newFiles) return;

    const filesArray = Array.from(newFiles);
    const totalFiles = files.length + filesArray.length;

    if (totalFiles > MAX_FILES) {
      enqueueSnackbar(`Máximo ${MAX_FILES} archivos permitidos. Seleccionaste ${totalFiles}.`, { variant: 'warning' });
      return;
    }

    // Validar formatos
    const invalidFiles = filesArray.filter(f => {
      const ext = f.name.toLowerCase();
      return !ext.endsWith('.csv') && !ext.endsWith('.xlsx') && !ext.endsWith('.xls');
    });

    if (invalidFiles.length > 0) {
      enqueueSnackbar('Solo se permiten archivos .csv, .xlsx o .xls', { variant: 'error' });
      return;
    }

    setFiles(prev => [...prev, ...filesArray]);
    enqueueSnackbar(`${filesArray.length} archivo(s) agregado(s)`, { variant: 'success' });
    
    // Reset input
    e.target.value = '';
  };

  const handleRemoveFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleEvaluate = async () => {
    if (!programaId) {
      enqueueSnackbar('Selecciona un programa', { variant: 'warning' });
      return;
    }

    if (files.length === 0) {
      enqueueSnackbar('Debes cargar al menos un archivo', { variant: 'warning' });
      return;
    }

    setEvaluating(true);
    try {
      const response = await verificarElegibilidadMasiva({
        historias: files,
        programa_id: programaId
      });

      const programaSeleccionado = programas.find(p => p.programa_id === programaId);

      const [pensumInfo, configInfo] = await Promise.all([
        obtenerPensumMetadata(programaId),
        obtenerConfiguracionMetadata(programaId)
      ]);

      guardarResultadosComparacion({
        response,
        metadata: {
          programaId,
          programaNombre: programaSeleccionado?.nombre_programa,
          pensumId: pensumInfo.pensumId,
          pensumMaterias: pensumInfo.pensumMaterias,
          semestreLimite: configInfo.semestreLimite,
          generadoEn: new Date().toISOString()
        }
      });

      enqueueSnackbar(`${response.total_estudiantes} estudiante(s) evaluado(s)`, { variant: 'success' });
      
      // Navegar a resultados
      navigate('/comparacion-resultados');
    } catch (err: any) {
      const msg = err?.message || 'Error al evaluar estudiantes';
      enqueueSnackbar(msg, { variant: 'error' });
    } finally {
      setEvaluating(false);
    }
  };

  const handleClear = () => {
    setFiles([]);
    setProgramaId(null);
  };

  return (
    <div className="min-h-full bg-gray-50">
      {/* Header azul */}
      <div className="bg-blue-900 text-white py-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-xl font-semibold">Comparación de Pensum</h2>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="max-w-4xl mx-auto p-8">
        <div className="bg-white rounded-xl shadow-sm border p-6">
          <h3 className="text-center text-blue-900 font-semibold mb-2">
            Ingrese las historias académicas de los estudiantes
          </h3>
          <p className="text-center text-sm text-gray-500 mb-6">
            Formatos permitidos: .CSV, .XLSX, .XLS (máximo {MAX_FILES} archivos)
          </p>

          {/* Selector de programa */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Programa Académico *
            </label>
            <select
              value={programaId ?? ''}
              onChange={(e) => setProgramaId(e.target.value ? Number(e.target.value) : null)}
              disabled={loadingProgramas}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Selecciona un programa</option>
              {programas.map(p => (
                <option key={p.programa_id} value={p.programa_id}>
                  {p.nombre_programa}
                </option>
              ))}
            </select>
          </div>

          {/* Lista de archivos cargados */}
          {files.length > 0 && (
            <div className="mb-4 p-4 bg-gray-50 rounded-lg border">
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-sm font-medium text-gray-700">
                  Archivos cargados ({files.length}/{MAX_FILES})
                </h4>
                <button
                  onClick={handleClear}
                  className="text-sm text-red-600 hover:text-red-700"
                >
                  Limpiar todo
                </button>
              </div>
              <div className="max-h-48 overflow-y-auto space-y-2">
                {files.map((file, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-2 bg-white rounded border text-sm"
                  >
                    <span className="truncate flex-1">{file.name}</span>
                    <button
                      onClick={() => handleRemoveFile(idx)}
                      className="ml-2 text-red-600 hover:text-red-700"
                      title="Eliminar"
                    >
                      <X size={16} />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Botones de carga y evaluación */}
          <div className="flex flex-col sm:flex-row items-center gap-3">
            <label className="flex-1 flex items-center justify-center gap-2 bg-gray-100 px-4 py-3 rounded-lg cursor-pointer hover:bg-gray-200 transition">
              <input
                type="file"
                accept=".csv,.xlsx,.xls"
                multiple
                onChange={handleFileChange}
                className="hidden"
                disabled={files.length >= MAX_FILES}
              />
              <Upload size={18} className="text-gray-600" />
              <span className="text-sm text-gray-700 font-medium">
                Cargar archivos ({files.length}/{MAX_FILES})
              </span>
            </label>

            <button
              onClick={handleEvaluate}
              disabled={evaluating || files.length === 0 || !programaId}
              className="flex-1 px-6 py-3 bg-blue-900 text-white rounded-lg hover:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
            >
              {evaluating ? 'Evaluando...' : 'Evaluar Estudiantes'}
            </button>
          </div>

          {/* Información adicional */}
          <div className="mt-6 flex items-start gap-2 text-sm text-blue-700 bg-blue-50 p-4 rounded-lg">
            <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium mb-1">Instrucciones:</p>
              <ul className="list-disc list-inside space-y-1 text-xs">
                <li>Selecciona el programa académico correspondiente</li>
                <li>Carga las historias académicas en formato CSV o Excel (.xlsx, .xls)</li>
                <li>El sistema comparará automáticamente cada historia con el pensum activo</li>
                <li>Nombre sugerido de archivos: Historia-Academica-CODIGO.csv o .xlsx</li>
                <li>Máximo {MAX_FILES} archivos por evaluación</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}