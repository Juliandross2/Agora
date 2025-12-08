import { getToken } from './Auth';

const BASE_URL = 'http://localhost:8000/api/configuracion';

export interface ConfiguracionActiva {
  configuracion_id: number;
  programa_id: number;
  programa_nombre: string;
  nota_aprobatoria: number;
  semestre_limite_electivas: number;
  es_activo: boolean;
  fecha_creacion: string;
  fecha_actualizacion: string;
}

export const obtenerConfiguracionActiva = async (
  programaId: number
): Promise<ConfiguracionActiva> => {
  const token = getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const url = new URL(BASE_URL);
  url.searchParams.set('programa_id', programaId.toString());

  const res = await fetch(url.toString(), {
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

  return data as ConfiguracionActiva;
};
