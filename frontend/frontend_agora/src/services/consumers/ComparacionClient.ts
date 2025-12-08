import { getToken } from './Auth';

const BASE_URL = 'http://localhost:8000/api/historias';

/** Resultado de comparación individual de un estudiante */
export interface MateriaAprobadaDespuesLimite {
  materia: string;
  semestre: number | null;
  creditos: number | null;
}

export interface ComparacionEstudiante {
  estudiante: string;
  semestre_maximo: number;
  creditos_aprobados: number;
  creditos_obligatorios_totales: number;
  periodos_matriculados: number;
  porcentaje_avance: number;
  nivelado: boolean;
  estado: number;
  materias_faltantes_hasta_semestre_limite: string[];
  materias_aprobadas_despues_semestre_limite: MateriaAprobadaDespuesLimite[];
}

/** Respuesta de verificación masiva */
export interface VerificacionMasivaResponse {
  total_estudiantes: number;
  elegibles: number;
  no_elegibles: number;
  resultados: ComparacionEstudiante[];
}

/** Payload para verificación masiva (FormData) */
export interface VerificacionMasivaPayload {
  historias: File[];
  programa_id: number;
}

/**
 * Verifica la elegibilidad de múltiples estudiantes mediante archivos CSV/Excel
 * POST /api/historias/verificar/masiva/
 * 
 * @param payload - Archivos de historias académicas y programa_id
 * @returns Respuesta con resultados de elegibilidad
 */
export const verificarElegibilidadMasiva = async (
  payload: VerificacionMasivaPayload
): Promise<VerificacionMasivaResponse> => {
  const token = getToken();
  if (!token) {
    throw new Error('No access token available');
  }

  // Crear FormData para enviar archivos
  const formData = new FormData();
  
  // Agregar cada archivo al FormData
  payload.historias.forEach((file) => {
    formData.append('historias', file);
  });
  
  // Agregar programa_id
  formData.append('programa_id', payload.programa_id.toString());

  const res = await fetch(`${BASE_URL}/verificar/masiva/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
      // No incluir 'Content-Type' - el navegador lo establece automáticamente con el boundary correcto
    },
    body: formData
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Error verificando elegibilidad masiva';
    throw new Error(msg);
  }

  return data as VerificacionMasivaResponse;
};

/**
 * Verifica la elegibilidad de un solo estudiante
 * POST /api/historias/verificar/
 * 
 * @param historia - Archivo CSV/Excel de la historia académica
 * @param programa_id - ID del programa académico
 * @returns Resultado de elegibilidad del estudiante
 */
export const verificarElegibilidadIndividual = async (
  historia: File,
  programa_id: number
): Promise<ComparacionEstudiante> => {
  const token = getToken();
  if (!token) {
    throw new Error('No access token available');
  }

  const formData = new FormData();
  formData.append('historia', historia);
  formData.append('programa_id', programa_id.toString());

  const res = await fetch(`${BASE_URL}/verificar/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Error verificando elegibilidad individual';
    throw new Error(msg);
  }

  return data as ComparacionEstudiante;
};