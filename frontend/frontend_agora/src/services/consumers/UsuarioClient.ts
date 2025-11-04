import type { User } from '../domain/UsuarioModels';
import { getToken } from './Auth';

export interface ProfileResponse {
  user: User;
}

const BASE_URL = 'http://localhost:8000/api/usuario';

/** Obtiene el perfil del usuario autenticado usando el access token almacenado */
export const getProfile = async (): Promise<ProfileResponse> => {
  const token = getToken();
  if (!token) {
    throw new Error('No access token available');
  }

  const res = await fetch(`${BASE_URL}/profile/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Error fetching profile';
    throw new Error(msg);
  }

  return data as ProfileResponse;
};

/** Respuesta esperada al desactivar un usuario */
export interface DeactivateResponse {
  message: string;
  user: User;
}

/** Desactiva un usuario */
export const desactivarUsuario = async (usuario_id: number): Promise<DeactivateResponse> => {
  const token = getToken();
  if (!token) {
    throw new Error('No access token available');
  }

  const res = await fetch(`${BASE_URL}/desactivar/`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ usuario_id })
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Error desactivando usuario';
    throw new Error(msg);
  }

  return data as DeactivateResponse;
};

/** Request/Response para registrar usuario */
export interface RegisterRequest {
  nombre_usuario: string;
  email_usuario: string;
  contrasenia: string;
  confirmar_contrasenia: string;
}

export interface RegisterResponse {
  message: string;
  user: User;
  refresh?: string;
  access?: string;
}

/** Registra un nuevo usuario (admin) */
export const registerUser = async (payload: RegisterRequest): Promise<RegisterResponse> => {
  const token = getToken(); // asume que se requiere estar autenticado para crear otro admin
  if (!token) {
    throw new Error('No access token available');
  }

  const res = await fetch(`${BASE_URL}/register/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Error registrando usuario';
    throw new Error(msg);
  }

  return data as RegisterResponse;
};