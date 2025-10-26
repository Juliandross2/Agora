/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login as authLogin } from '../services/consumers/Auth';
import type { LoginRequest } from '../services/domain/TokenModels';

export default function Login() {
  const [email, setEmail] = useState('john.doe@example.com');
  const [password, setPassword] = useState('MiPassword123!');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const payload: LoginRequest = {
      email_usuario: email,
      contrasenia: password,
    };

    try {
      await authLogin(payload); // authLogin guarda el access token
      navigate('/home');
    } catch (err: any) {
      setError(err?.message || 'Error en login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-blue-900">
      {/* Contenedor centrado que alinea header y tarjeta de login */}
      <div className="w-full flex flex-col items-center px-6">
        {/* Header centrado sobre la tarjeta (alineado con la tarjeta por max-w-sm) */}
        <header className="w-full max-w-lg flex items-center gap-4 justify-center mt-6">
          <img src="/unicauca_logo.svg" alt="Universidad del Cauca" className="h-24" />
          <div className="h-10 border-l border-white/30 pl-4 flex items-center text-white font-semibold text-lg">
            Sistema AGORA
          </div>
        </header>

        <div className="w-full max-w-sm bg-white rounded-2xl shadow-xl p-8 mt-8">
          <div className="flex flex-col items-center mb-6">
            {/* Logo / header */}
            <div className="w-40 h-40 rounded-full bg-gray-100 flex items-center justify-center mb-4">
              <img src="/agora_logo.svg" alt="Agora" className="w-40 h-40" />
            </div>
            <h2 className="text-xl font-semibold text-blue-900">Iniciar Sesión</h2>
          </div>

          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="sr-only">Usuario</label>
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                type="email"
                placeholder="Usuario"
                required
                className="w-full px-4 py-3 rounded-lg bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
            </div>

            <div>
              <label className="sr-only">Contraseña</label>
              <input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                placeholder="Contraseña"
                required
                className="w-full px-4 py-3 rounded-lg bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
            </div>

            {error && <div className="text-sm text-red-600">{error}</div>}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition disabled:opacity-60"
            >
              {loading ? 'Ingresando...' : 'Entrar'}
            </button>

            <div className="text-center text-xs text-blue-700">
              <a href="#" onClick={(e) => e.preventDefault()} className="underline">¿Olvidaste tu contraseña?</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}