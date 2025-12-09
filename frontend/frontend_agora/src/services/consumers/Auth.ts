import type { LoginRequest, LoginResponse } from "../domain/TokenModels";

const BASE_URL = 'http://localhost:8000/api/usuario';
const TOKEN_KEY = 'token';

/** Decodifica un JWT (sin verificar firma) */
const decodeToken = (token: string): any | null => {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const payload = parts[1];
    const decoded = JSON.parse(atob(payload));
    return decoded;
  } catch (e) {
    return null;
  }
};

/** Guarda el access token en localStorage */
export const setToken = (token: string) => {
  localStorage.setItem(TOKEN_KEY, token);
};

/** Recupera el access token desde localStorage */
export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

/** Elimina el token */
export const clearToken = () => {
  localStorage.removeItem(TOKEN_KEY);
};

/** Valida si el token existe y es válido */
export const isTokenValid = (token?: string | null): boolean => {
  const t = token ?? getToken();
  return !!t;
};

/** Obtiene el claim es_admin del token (false si no existe o es inválido) */
export const isAdmin = (token?: string | null): boolean => {
  const t = token ?? getToken();
  if (!t) return false;
  const decoded = decodeToken(t);
  return decoded?.es_admin === true;
};

/** Obtiene toda la información decodificada del token */
export const getTokenPayload = (token?: string | null): any | null => {
  const t = token ?? getToken();
  if (!t) return null;
  return decodeToken(t);
};

/** Ejecuta login y guarda el access token si viene en la respuesta */
export const login = async (payload: LoginRequest): Promise<LoginResponse> => {
  const res = await fetch(`${BASE_URL}/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data?.error || data?.detail || 'Login failed';
    throw new Error(msg);
  }

  if (data?.access) {
    setToken(data.access);
  }

  return data as LoginResponse;
};