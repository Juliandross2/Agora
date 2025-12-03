import type { VerificacionMasivaResponse } from '../services/consumers/ComparacionClient';

const STORAGE_KEY = 'comparacion_resultados';

/**
 * Guarda los resultados de comparación en sessionStorage
 */
export const guardarResultadosComparacion = (resultados: VerificacionMasivaResponse): void => {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(resultados));
  } catch (error) {
    console.error('Error al guardar resultados en sessionStorage:', error);
  }
};

/**
 * Obtiene los resultados de comparación desde sessionStorage
 */
export const obtenerResultadosComparacion = (): VerificacionMasivaResponse | null => {
  try {
    const data = sessionStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : null;
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