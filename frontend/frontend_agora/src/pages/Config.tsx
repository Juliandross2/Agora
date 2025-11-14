import React, { useEffect, useState } from 'react';
import { useSnackbar } from 'notistack';
import { UserPlus } from 'lucide-react';
import { getProfile, desactivarUsuario, listarUsuarios, activarUsuario } from '../services/consumers/UsuarioClient';
import { clearToken } from '../services/consumers/Auth';
import type { User } from '../services/domain/UsuarioModels';
import ConfirmDialog from '../components/ConfirmDialog';
import RegisterFormDialog from '../components/RegisterFormDialog';
import { useActiveSection } from '../DashboardLayout';

export default function Config() {
  const { setActiveSection } = useActiveSection();
  useEffect(() => { setActiveSection('configuracion'); }, [setActiveSection]);

  const { enqueueSnackbar } = useSnackbar();
  const [profile, setProfile] = useState<User | null>(null);
  const [loadingProfile, setLoadingProfile] = useState(false);
  const [deactLoading, setDeactLoading] = useState(false);

  // estado para mostrar diálogo (propio)
  const [showConfirmDeactivate, setShowConfirmDeactivate] = useState(false);

  // lista de usuarios
  const [users, setUsers] = useState<User[]>([]);
  const [usersLoading, setUsersLoading] = useState(false);
  const [usersError, setUsersError] = useState<string | null>(null);

  // desactivar otro usuario
  const [selectedUserToDeactivate, setSelectedUserToDeactivate] = useState<User | null>(null);
  const [showConfirmDeactivateUser, setShowConfirmDeactivateUser] = useState(false);
  const [deactUserLoading, setDeactUserLoading] = useState(false);

  // --- estado para activar usuarios ---
  const [actUserLoading, setActUserLoading] = useState(false);

  // --- estado para registro de usuarios ---
  const [showRegisterDialog, setShowRegisterDialog] = useState(false);

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

  useEffect(() => {
    let mounted = true;
    const loadUsers = async () => {
      setUsersLoading(true);
      setUsersError(null);
      try {
        const list = await listarUsuarios();
        if (!mounted) return;
        setUsers(list);
      } catch (e: any) {
        if (!mounted) return;
        const msg = e?.message || 'Error al cargar usuarios';
        setUsersError(msg);
        enqueueSnackbar(msg, { variant: 'error' });
      } finally {
        if (mounted) setUsersLoading(false);
      }
    };
    loadUsers();
    return () => { mounted = false; };
  }, [enqueueSnackbar]);

  // abrir diálogo en lugar de window.confirm (propia cuenta)
  const handleDeactivate = async () => {
    if (!profile) return;
    setShowConfirmDeactivate(true);
  };

  // acción que ejecuta la desactivación cuando confirman (propia cuenta)
  const onConfirmDeactivate = async () => {
    if (!profile) return;
    setShowConfirmDeactivate(false);
    setDeactLoading(true);
    try {
      const res = await desactivarUsuario(profile.usuario_id);
      enqueueSnackbar(res.message || 'Cuenta desactivada', { variant: 'success' });
      // limpiar token y redirigir
      clearToken();
      window.location.href = '/login';
    } catch (e: any) {
      const msg = e?.message || 'Error al desactivar cuenta';
      enqueueSnackbar(msg, { variant: 'error' });
    } finally {
      setDeactLoading(false);
    }
  };

  // abrir diálogo para desactivar otro usuario
  const handleDeactivateUser = (user: User) => {
    setSelectedUserToDeactivate(user);
    setShowConfirmDeactivateUser(true);
  };

  // --- activar usuario directamente ---
  const handleActivateUser = async (user: User) => {
    setActUserLoading(true);
    try {
      const res = await activarUsuario(user.usuario_id);
      enqueueSnackbar(res.message || 'Usuario activado', { variant: 'success' });
      const list = await listarUsuarios();
      setUsers(list);
    } catch (e: any) {
      const msg = e?.message || 'Error al activar usuario';
      enqueueSnackbar(msg, { variant: 'error' });
    } finally {
      setActUserLoading(false);
    }
  };

  const onConfirmDeactivateUser = async () => {
    if (!selectedUserToDeactivate) return;
    setShowConfirmDeactivateUser(false);
    setDeactUserLoading(true);
    try {
      const res = await desactivarUsuario(selectedUserToDeactivate.usuario_id);
      enqueueSnackbar(res.message || 'Usuario desactivado', { variant: 'success' });
      // refrescar lista de usuarios
      const list = await listarUsuarios();
      setUsers(list);
    } catch (e: any) {
      const msg = e?.message || 'Error al desactivar usuario';
      enqueueSnackbar(msg, { variant: 'error' });
    } finally {
      setDeactUserLoading(false);
      setSelectedUserToDeactivate(null);
    }
  };

  const handleUserRegistered = (updatedUsers: User[]) => {
    setUsers(updatedUsers);
  };

  return (
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
      </div>

      {/* Lista de usuarios */}
      <div className="bg-white rounded-xl p-6 shadow border">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-semibold">Usuarios</h2>
            <p className="text-sm text-gray-500">{users.length} en total</p>
          </div>
          <button
            onClick={() => setShowRegisterDialog(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-900 text-white rounded-md hover:bg-blue-800 transition"
          >
            <UserPlus className="w-4 h-4" />
            Agregar Usuario
          </button>
        </div>

        {usersLoading && <div className="text-center text-gray-600">Cargando usuarios...</div>}
        {usersError && <div className="text-center text-red-600">{usersError}</div>}

        {!usersLoading && !usersError && (
          <div className="space-y-3">
            {users.map((u) => (
              <div key={u.usuario_id} className="flex items-center gap-4 p-3 border rounded-lg hover:shadow-sm transition">
                <div className="w-12 h-12 bg-blue-900 text-white rounded-full flex items-center justify-center font-semibold">
                  {String(u.nombre_usuario).split(' ').map(n => n[0]).slice(0,2).join('').toUpperCase()}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <div className="truncate">
                      <div className="text-sm font-medium text-gray-800">{u.nombre_usuario}</div>
                      <div className="text-xs text-gray-500 truncate">{u.email_usuario}</div>
                    </div>
                    <div className="ml-4 text-right">
                      <div className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${u.es_activo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                        {u.es_activo ? 'Activo' : 'Inactivo'}
                      </div>
                    </div>
                  </div>

                  <div className="mt-2 flex items-center gap-2">
                    {/* Si está inactivo permitir activarlo */}
                    {!u.es_activo ? (
                      <button
                        onClick={() => handleActivateUser(u)}
                        disabled={actUserLoading}
                        className="px-3 py-1 text-sm rounded-md bg-green-600 text-white hover:bg-green-700 disabled:opacity-60"
                      >
                        {actUserLoading ? 'Procesando...' : 'Activar'}
                      </button>
                    ) : (
                      <div className="text-xs text-gray-500"></div>
                    )}

                    {/* nota si es tu cuenta */}
                    {profile && profile.usuario_id === u.usuario_id && (
                      <div className="text-xs text-gray-500"> (es tu cuenta)</div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Dialogs */}
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

      <ConfirmDialog
        isOpen={showConfirmDeactivateUser}
        title="Desactivar usuario"
        description={selectedUserToDeactivate ? `Desactivar a ${selectedUserToDeactivate.nombre_usuario}?` : 'Desactivar usuario?'}
        confirmLabel="Desactivar"
        cancelLabel="Cancelar"
        loading={deactUserLoading}
        onConfirm={onConfirmDeactivateUser}
        onCancel={() => { setShowConfirmDeactivateUser(false); setSelectedUserToDeactivate(null); }}
      />

      <RegisterFormDialog
        isOpen={showRegisterDialog}
        onClose={() => setShowRegisterDialog(false)}
        onUserRegistered={handleUserRegistered}
      />
    </div>
  );
}