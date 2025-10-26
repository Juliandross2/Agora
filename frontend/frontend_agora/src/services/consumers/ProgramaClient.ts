import { apiProgramaResponse } from '../domain/ProgramaModels';
import { getToken } from './Auth';


const BASE_URL = 'http://localhost:8000/api/programa';

/** Listar programas */
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
    const msg = data?.error || data?.detail || 'Error fetching profile';
    throw new Error(msg);
  }

  return data as apiProgramaResponse;
};