import type { LoginRequest, LoginResponse } from "../domain/TokenModels";

const BASE_URL = 'http://localhost:8000/api/usuario';
const TOKEN_KEY = 'token';

/** Guarda el access token en localStorage */
export const setToken = (token: string) => {
  localStorage.setItem(TOKEN_KEY, token);
};

// simple validator: por ahora considera válido si existe token (localStorage)
export const isTokenValid = (token?: string | null): boolean => {
  const t = token ?? getToken();
  return !!t;
};

/** Recupera el access token desde localStorage */
export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

/** Elimina el token */
export const clearToken = () => {
  localStorage.removeItem(TOKEN_KEY);
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
    // Lanza el mensaje de error del backend o un genérico
    const msg = data?.error || data?.detail || 'Login failed';
    throw new Error(msg);
  }

  if (data?.access) {
    setToken(data.access);
  }

  return data as LoginResponse;
};