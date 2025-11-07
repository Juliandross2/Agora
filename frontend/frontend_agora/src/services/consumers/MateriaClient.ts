import type { Materia } from '../domain/PensumModels';
import { getToken } from './Auth';

const MATERIA_BASE_URL = 'http://localhost:8000/api/materia';

export interface MateriaCreatePayload {
  pensum_id: number;
  nombre_materia: string;
  creditos: number;
  semestre: number;
  es_obligatoria?: boolean;
  es_activa?: boolean;
}

export interface CrearMateriaResponse {
  message: string;
  materia: Materia;
}

/**
 * Crea una nueva materia.
 * POST {{base_url}}/api/materia/crear/
 */
export const crearMateria = async (payload: MateriaCreatePayload): Promise<CrearMateriaResponse> => {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${MATERIA_BASE_URL}/crear/`, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload),
  });

  let data: any;
  try {
    data = await res.json();
  } catch (err) {
    throw new Error('Invalid response from crear materia API');
  }

  // éxito esperado
  if (res.status === 201) {
    return {
      message: data?.message || 'Materia creada exitosamente',
      materia: data?.materia as Materia,
    };
  }

  // manejar errores de validación / negocio
  const msg = data?.error || data?.detail || data?.message || 'Error creating materia';
  throw new Error(msg);
};