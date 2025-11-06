import { apiProgramaResponse, Programa } from '../domain/ProgramaModels';
import { getToken } from './Auth';

const BASE_URL = 'http://localhost:8000/api/programa';

/** Listar todos los programas */
export const listarProgramas = async (): Promise<apiProgramaResponse> => {
  const token = getToken();
  if (!token) {
    throw new Error('No access token available');
  }

  const res = await fetch(`${BASE_URL}/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Error fetching programs';
    throw new Error(msg);
  }

  return data as apiProgramaResponse;
};

/** Obtener programa por ID */
export const obtenerPrograma = async (programa_id: number): Promise<{ programa: Programa; message: string }> => {
  const token = getToken();
  if (!token) {
    throw new Error('No access token available');
  }

  const res = await fetch(`${BASE_URL}/${programa_id}/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Error fetching program';
    throw new Error(msg);
  }

  return data;
};

/** Buscar programas por nombre */
export const buscarProgramas = async (nombre: string): Promise<apiProgramaResponse> => {
  const token = getToken();
  if (!token) {
    throw new Error('No access token available');
  }

  try {
    const res = await fetch(`${BASE_URL}/buscar/?nombre=${encodeURIComponent(nombre)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await res.json();

    if (!res.ok) {
      const msg = data?.error || data?.detail || 'Error searching programs';
      throw new Error(msg);
    }

    return data as apiProgramaResponse;
  } catch (error: any) {
    console.error('Error en buscarProgramas:', error);
    throw error;
  }
};

/** Crear programa */
export const crearPrograma = async (programa: { nombre_programa: string }): Promise<{ programa: Programa; message: string }> => {
  const token = getToken();
  if (!token) {
    throw new Error('No access token available');
  }

  const res = await fetch(`${BASE_URL}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(programa)
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Error creating program';
    throw new Error(msg);
  }

  return data;
};

/** Actualizar programa */
export const actualizarPrograma = async (programa_id: number, programa: { nombre_programa: string }): Promise<{ programa: Programa; message: string }> => {
  const token = getToken();
  if (!token) {
    throw new Error('No access token available');
  }

  const res = await fetch(`${BASE_URL}/${programa_id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(programa)
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Error updating program';
    throw new Error(msg);
  }

  return data;
};

/** Eliminar programa */
export const eliminarPrograma = async (programa_id: number): Promise<{ message: string }> => {
  const token = getToken();
  if (!token) {
    throw new Error('No access token available');
  }

  const res = await fetch(`${BASE_URL}/${programa_id}/`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Error deleting program';
    throw new Error(msg);
  }

  return data;
};