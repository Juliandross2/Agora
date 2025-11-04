import React, { useEffect, useState } from 'react';
import DashboardLayout from '../DashboardLayout';
import { getProfile, desactivarUsuario, registerUser } from '../services/consumers/UsuarioClient';
import { clearToken } from '../services/consumers/Auth';
import type { User } from '../services/domain/UsuarioModels';
import ConfirmDialog from '../components/ConfirmDialog'; // <-- agregado

export default function Config() {
  const [profile, setProfile] = useState<User | null>(null);
  const [loadingProfile, setLoadingProfile] = useState(false);
  const [deactLoading, setDeactLoading] = useState(false);
  const [deactError, setDeactError] = useState<string | null>(null);
  const [deactSuccess, setDeactSuccess] = useState<string | null>(null);

  // estado para mostrar diálogo
  const [showConfirmDeactivate, setShowConfirmDeactivate] = useState(false);

  // register form
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [regLoading, setRegLoading] = useState(false);
  const [regError, setRegError] = useState<string | null>(null);
  const [regSuccess, setRegSuccess] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoadingProfile(true);
      try {
        const res = await getProfile();
        if (!mounted) return;
        setProfile(res.user);
      } catch (e: any) {
        setProfile(null);
      } finally {
        if (mounted) setLoadingProfile(false);
      }
    };
    load();
    return () => { mounted = false; };
  }, []);

  // abrir diálogo en lugar de window.confirm
  const handleDeactivate = async () => {
    if (!profile) return;
    setShowConfirmDeactivate(true);
  };

  // acción que ejecuta la desactivación cuando confirman
  const onConfirmDeactivate = async () => {
    if (!profile) return;
    setShowConfirmDeactivate(false);
    setDeactError(null);
    setDeactSuccess(null);
    setDeactLoading(true);
    try {
      const res = await desactivarUsuario(profile.usuario_id);
      setDeactSuccess(res.message || 'Cuenta desactivada');
      // limpiar token y redirigir
      clearToken();
      window.location.href = '/login';
    } catch (e: any) {
      setDeactError(e?.message || 'Error al desactivar cuenta');
    } finally {
      setDeactLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setRegError(null);
    setRegSuccess(null);

    if (!nombre || !email || !password || !confirm) {
      setRegError('Completa todos los campos');
      return;
    }
    if (password !== confirm) {
      setRegError('Las contraseñas no coinciden');
      return;
    }

    setRegLoading(true);
    try {
      const payload = {
        nombre_usuario: nombre,
        email_usuario: email,
        contrasenia: password,
        confirmar_contrasenia: confirm
      };
      const res = await registerUser(payload);
      setRegSuccess(res.message || 'Usuario registrado');
      // limpiar formulario
      setNombre('');
      setEmail('');
      setPassword('');
      setConfirm('');
    } catch (e: any) {
      setRegError(e?.message || 'Error registrando usuario');
    } finally {
      setRegLoading(false);
    }
  };

  return (
    <DashboardLayout>
      {(activeSection) => (
        <div className="p-8 space-y-6">
          <div className="bg-white rounded-xl p-6 shadow border">
            <h2 className="text-xl font-semibold mb-2">Configuración de cuenta</h2>
            <p className="text-sm text-gray-600 mb-4">
              Información de la cuenta actual.
            </p>

            <div className="flex items-center gap-4">
              <div className="flex-1">
                <div className="text-lg font-medium">
                  {loadingProfile ? 'Cargando...' : (profile?.nombre_usuario ?? 'Sin nombre')}
                </div>
                <div className="text-sm text-gray-500">{profile?.email_usuario ?? ''}</div>
                <div className="text-sm text-gray-400 mt-2">
                  Estado: {profile?.es_activo ? <span className="text-green-600">Activo</span> : <span className="text-red-600">Inactivo</span>}
                </div>
              </div>

              <div>
                <button
                  onClick={handleDeactivate}
                  disabled={deactLoading}
                  className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-60"
                >
                  {deactLoading ? 'Desactivando...' : 'Desactivar mi cuenta'}
                </button>
              </div>
            </div>

            {deactError && <div className="mt-3 text-sm text-red-600">{deactError}</div>}
            {deactSuccess && <div className="mt-3 text-sm text-green-600">{deactSuccess}</div>}
          </div>

          <div className="bg-white rounded-xl p-6 shadow border">
            <h2 className="text-xl font-semibold mb-4">Registrar otro administrador</h2>

            <form onSubmit={handleRegister} className="space-y-3 max-w-md">
              <div>
                <label className="block text-sm font-medium text-gray-700">Nombre</label>
                <input
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  className="mt-1 w-full rounded-md border px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Correo</label>
                <input
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  type="email"
                  className="mt-1 w-full rounded-md border px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Contraseña</label>
                <input
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  type="password"
                  className="mt-1 w-full rounded-md border px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Confirmar contraseña</label>
                <input
                  value={confirm}
                  onChange={(e) => setConfirm(e.target.value)}
                  type="password"
                  className="mt-1 w-full rounded-md border px-3 py-2"
                  required
                />
              </div>

              <div className="flex items-center gap-3">
                <button
                  type="submit"
                  disabled={regLoading}
                  className="px-4 py-2 bg-blue-900 text-white rounded-md hover:bg-blue-800 disabled:opacity-60"
                >
                  {regLoading ? 'Registrando...' : 'Registrar administrador'}
                </button>

                {regError && <div className="text-sm text-red-600">{regError}</div>}
                {regSuccess && <div className="text-sm text-green-600">{regSuccess}</div>}
              </div>
            </form>
          </div>

          {/* Confirm dialog */}
          <ConfirmDialog
            isOpen={showConfirmDeactivate}
            title="Desactivar cuenta"
            description="¿Confirmas desactivar tu cuenta? Esto cerrará tu sesión inmediatamente."
            confirmLabel="Desactivar"
            cancelLabel="Cancelar"
            loading={deactLoading}
            onConfirm={onConfirmDeactivate}
            onCancel={() => setShowConfirmDeactivate(false)}
          />
        </div>
      )}
    </DashboardLayout>
  );
}