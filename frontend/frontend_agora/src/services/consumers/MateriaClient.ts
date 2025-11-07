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

export interface MateriaUpdatePayload {
  nombre_materia?: string;
  creditos?: number;
  semestre?: number;
  es_obligatoria?: boolean;
  es_activa?: boolean;
  pensum_id?: number;
}

export interface ActualizarMateriaResponse {
  message: string;
  materia: Materia;
}

/**
 * Actualiza parcialmente una materia.
 * PATCH {{base_url}}/api/materia/{materia_id}/patch/
 */
export const patchMateria = async (
  materia_id: number,
  payload: MateriaUpdatePayload
): Promise<ActualizarMateriaResponse> => {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${MATERIA_BASE_URL}/${materia_id}/patch/`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify(payload),
  });

  let data: any;
  try {
    data = await res.json();
  } catch (err) {
    throw new Error('Invalid response from patch materia API');
  }

  if (res.status === 200) {
    return {
      message: data?.message || 'Materia actualizada exitosamente',
      materia: data?.materia as Materia,
    };
  }

  // manejar errores (400, 404, otros)
  const errDetail =
    data?.error ||
    data?.detail ||
    (data && typeof data === 'object' ? JSON.stringify(data) : null) ||
    `HTTP ${res.status}`;
  throw new Error(errDetail);
};