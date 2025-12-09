import { getToken } from './Auth';

const BASE_URL = 'http://localhost:8000/api/configuracion';

export interface Configuracion {
  configuracion_id: number;
  programa_id: number;
  programa_nombre: string;
  nota_aprobatoria: number;
  semestre_limite_electivas: number;
  es_activo: boolean;
  fecha_creacion: string;
  fecha_actualizacion: string;
}

// Alias para compatibilidad
export type ConfiguracionActiva = Configuracion;

export interface CrearConfiguracionPayload {
  programa_id: number;
  nota_aprobatoria: number;
  semestre_limite_electivas: number;
}

export interface ActualizarConfiguracionPayload {
  nota_aprobatoria?: number;
  semestre_limite_electivas?: number;
}

export const obtenerConfiguracionPrograma = async (
  programaId: number
): Promise<Configuracion> => {
  const token = getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const url = `${BASE_URL}/programa/${programaId}/`;

  const res = await fetch(url, {
    method: 'GET',
    headers,
  });

  let data: any;
  try {
    data = await res.json();
  } catch (error) {
    throw new Error('Respuesta inválida del servicio de configuración');
  }

  if (!res.ok) {
    const message = data?.error || data?.detail || 'Error al obtener configuración';
    throw new Error(message);
  }

  return data as Configuracion;
};

// Alias para compatibilidad
export const obtenerConfiguracionActiva = obtenerConfiguracionPrograma;

export const crearConfiguracion = async (
  payload: CrearConfiguracionPayload
): Promise<Configuracion> => {
  const token = getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE_URL}/crear/`, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload),
  });

  let data: any;
  try {
    data = await res.json();
  } catch (error) {
    throw new Error('Respuesta inválida del servicio de configuración');
  }

  if (!res.ok) {
    const message = data?.error || data?.detail || 'Error al crear configuración';
    throw new Error(message);
  }

  return data as Configuracion;
};

export const actualizarConfiguracion = async (
  configuracionId: number,
  payload: ActualizarConfiguracionPayload
): Promise<Configuracion> => {
  const token = getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE_URL}/${configuracionId}/actualizar/`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(payload),
  });

  let data: any;
  try {
    data = await res.json();
  } catch (error) {
    throw new Error('Respuesta inválida del servicio de configuración');
  }

  if (!res.ok) {
    const message = data?.error || data?.detail || 'Error al actualizar configuración';
    throw new Error(message);
  }

  return data as Configuracion;
};

export const eliminarConfiguracion = async (
  configuracionId: number
): Promise<{ message: string }> => {
  const token = getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE_URL}/${configuracionId}/`, {
    method: 'DELETE',
    headers,
  });

  let data: any;
  try {
    data = await res.json();
  } catch (error) {
    throw new Error('Respuesta inválida del servicio de configuración');
  }

  if (!res.ok) {
    const message = data?.error || data?.detail || 'Error al eliminar configuración';
    throw new Error(message);
  }

  return data as { message: string };
};
