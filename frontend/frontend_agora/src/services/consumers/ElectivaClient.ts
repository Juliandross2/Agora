import { ElectivaCreatePayload, CrearElectivaResponse, Electiva, ElectivaUpdatePayload, ActualizarElectivaResponse, EliminarElectivaResponse, ListarElectivasResponse } from '../domain/ElectivaModels';
import { getToken } from './Auth';

const ELECTIVA_BASE_URL = 'http://localhost:8000/api/electiva';

/**
 * Crear nueva electiva
 * POST {{base_url}}/api/electiva/crear/
 */
export const crearElectiva = async (payload: ElectivaCreatePayload): Promise<CrearElectivaResponse> => {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${ELECTIVA_BASE_URL}/crear/`, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload),
  });

  let data: any;
  try {
    data = await res.json();
  } catch {
    throw new Error('Invalid response from crear electiva API');
  }

  if (res.status === 201) {
    return {
      message: data?.message || 'Electiva creada exitosamente',
      electiva: data?.electiva as Electiva,
    };
  }

  const msg = data?.error || data?.detail || data?.message || `HTTP ${res.status}`;
  throw new Error(msg);
};

/**
 * Actualizar electiva existente (PUT)
 * PUT {{base_url}}/api/electiva/{electiva_id}/actualizar/
 */
export const actualizarElectiva = async (
  electiva_id: number,
  payload: ElectivaUpdatePayload
): Promise<ActualizarElectivaResponse> => {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${ELECTIVA_BASE_URL}/${electiva_id}/actualizar/`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(payload),
  });

  let data: any;
  try {
    data = await res.json();
  } catch {
    throw new Error('Invalid response from actualizar electiva API');
  }

  if (res.status === 200) {
    return {
      message: data?.message || 'Electiva actualizada exitosamente',
      electiva: data?.electiva as Electiva,
    };
  }

  const errDetail =
    data?.error ||
    data?.detail ||
    data?.message ||
    (data && typeof data === 'object' ? JSON.stringify(data) : null) ||
    `HTTP ${res.status}`;
  throw new Error(errDetail);
};

/**
 * Eliminar (soft delete) electiva
 * DELETE {{base_url}}/api/electiva/{electiva_id}/eliminar/
 */
export const eliminarElectiva = async (electiva_id: number): Promise<EliminarElectivaResponse> => {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${ELECTIVA_BASE_URL}/${electiva_id}/eliminar/`, {
    method: 'DELETE',
    headers,
  });

  let data: any = null;
  try {
    data = await res.json();
  } catch {
    // respuesta sin JSON
  }

  if (res.status === 200) {
    return { message: data?.message || 'Electiva marcada como inactiva' };
  }

  const errMsg =
    data?.error ||
    data?.detail ||
    data?.message ||
    (data && typeof data === 'object' ? JSON.stringify(data) : null) ||
    `HTTP ${res.status}`;
  throw new Error(errMsg);
};

/**
 * Listar electivas activas
 * GET {{base_url}}/api/electiva/activas/
 */
export const listarElectivasActivas = async (): Promise<ListarElectivasResponse> => {
  const token = getToken();
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${ELECTIVA_BASE_URL}/activas/`, {
    method: 'GET',
    headers,
  });

  let data: any;
  try {
    data = await res.json();
  } catch {
    throw new Error('Invalid response from listar electivas activas API');
  }

  if (!res.ok) {
    const msg = data?.error || data?.detail || data?.message || `HTTP ${res.status}`;
    throw new Error(msg);
  }

  return {
    message: data?.message || 'Electivas activas obtenidas exitosamente',
    electivas: (data?.electivas || []) as Electiva[],
    total: typeof data?.total === 'number' ? data.total : (data?.electivas ? (data.electivas.length || 0) : 0),
  };
};