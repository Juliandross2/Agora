import type { VerificacionMasivaResponse } from '../services/consumers/ComparacionClient';
import type { PensumMateriaResumen } from './pensumUtils';

const STORAGE_KEY = 'comparacion_resultados';

export interface ComparacionResultadosMetadata {
  programaId: number;
  programaNombre?: string;
  pensumId?: number | null;
  pensumMaterias?: PensumMateriaResumen[];
  semestreLimite?: number | null;
  generadoEn?: string;
}

export interface ComparacionResultadosCache {
  response: VerificacionMasivaResponse;
  metadata: ComparacionResultadosMetadata;
}

/**
 * Guarda los resultados de comparación en sessionStorage
 */
export const guardarResultadosComparacion = (payload: ComparacionResultadosCache): void => {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch (error) {
    console.error('Error al guardar resultados en sessionStorage:', error);
  }
};

/**
 * Obtiene los resultados de comparación desde sessionStorage
 */
export const obtenerResultadosComparacion = (): ComparacionResultadosCache | null => {
  try {
    const data = sessionStorage.getItem(STORAGE_KEY);
    if (!data) return null;

    const parsed = JSON.parse(data);

    if (parsed?.response && parsed?.metadata) {
      return parsed as ComparacionResultadosCache;
    }

    // Compatibilidad con versiones anteriores (solo respuesta)
    if (parsed?.total_estudiantes !== undefined) {
      return {
        response: parsed as VerificacionMasivaResponse,
        metadata: {
          programaId: 0,
          generadoEn: new Date().toISOString(),
        },
      };
    }

    return null;
  } catch (error) {
    console.error('Error al obtener resultados de sessionStorage:', error);
    return null;
  }
};

/**
 * Limpia los resultados de comparación de sessionStorage
 */
export const limpiarResultadosComparacion = (): void => {
  try {
    sessionStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.error('Error al limpiar resultados de sessionStorage:', error);
  }
};