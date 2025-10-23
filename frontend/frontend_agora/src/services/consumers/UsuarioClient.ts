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