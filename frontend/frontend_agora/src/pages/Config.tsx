import React, { useEffect, useState } from 'react';
import { useSnackbar } from 'notistack';
import { UserPlus, Settings, Edit2, Trash2 } from 'lucide-react';
import { getProfile, desactivarUsuario, listarUsuarios, activarUsuario } from '../services/consumers/UsuarioClient';
import { obtenerConfiguracionPrograma, eliminarConfiguracion } from '../services/consumers/ConfiguracionClient';
import { listarProgramas } from '../services/consumers/ProgramaClient';
import { clearToken } from '../services/consumers/Auth';
import type { User } from '../services/domain/UsuarioModels';
import type { Programa } from '../services/domain/ProgramaModels';
import type { Configuracion } from '../services/consumers/ConfiguracionClient';
import ConfirmDialog from '../components/ConfirmDialog';
import RegisterFormDialog from '../components/RegisterFormDialog';
import ConfiguracionFormDialog from '../components/ConfiguracionFormDialog';
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

  // --- estado para configuración de programas ---
  const [programas, setProgramas] = useState<Programa[]>([]);
  const [programasLoading, setProgramasLoading] = useState(false);
  const [programasError, setProgramasError] = useState<string | null>(null);

  // configuraciones por programa
  const [configuraciones, setConfiguraciones] = useState<Map<number, Configuracion | null>>(new Map());
  const [configLoadingMap, setConfigLoadingMap] = useState<Map<number, boolean>>(new Map());

  // diálogo de configuración
  const [showConfigDialog, setShowConfigDialog] = useState(false);
  const [selectedPrograma, setSelectedPrograma] = useState<Programa | null>(null);
  const [selectedConfig, setSelectedConfig] = useState<Configuracion | null>(null);

  // diálogo de confirmación para eliminar
  const [showConfirmDeleteConfig, setShowConfirmDeleteConfig] = useState(false);
  const [configToDelete, setConfigToDelete] = useState<Configuracion | null>(null);
  const [deleteConfigLoading, setDeleteConfigLoading] = useState(false);

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

  // cargar programas
  useEffect(() => {
    let mounted = true;
    const loadProgramas = async () => {
      setProgramasLoading(true);
      setProgramasError(null);
      try {
        const response = await listarProgramas();
        if (!mounted) return;
        setProgramas(response.programas);
      } catch (e: any) {
        if (!mounted) return;
        const msg = e?.message || 'Error al cargar programas';
        setProgramasError(msg);
        enqueueSnackbar(msg, { variant: 'error' });
      } finally {
        if (mounted) setProgramasLoading(false);
      }
    };
    loadProgramas();
    return () => { mounted = false; };
  }, [enqueueSnackbar]);

  // cargar configuración de un programa
  const loadConfiguracion = async (programaId: number) => {
    setConfigLoadingMap(prev => new Map(prev).set(programaId, true));
    try {
      const config = await obtenerConfiguracionPrograma(programaId);
      setConfiguraciones(prev => new Map(prev).set(programaId, config));
    } catch (e: any) {
      // Si no existe configuración, simplemente guardamos null
      setConfiguraciones(prev => new Map(prev).set(programaId, null));
    } finally {
      setConfigLoadingMap(prev => new Map(prev).set(programaId, false));
    }
  };

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

  // handlers para configuración
  const handleEditConfig = (programa: Programa) => {
    setSelectedPrograma(programa);
    const config = configuraciones.get(programa.programa_id) || null;
    setSelectedConfig(config);
    setShowConfigDialog(true);
  };

  const handleDeleteConfig = (config: Configuracion) => {
    setConfigToDelete(config);
    setShowConfirmDeleteConfig(true);
  };

  const onConfirmDeleteConfig = async () => {
    if (!configToDelete) return;
    setShowConfirmDeleteConfig(false);
    setDeleteConfigLoading(true);
    try {
      await eliminarConfiguracion(configToDelete.configuracion_id);
      enqueueSnackbar('Configuración eliminada correctamente', { variant: 'success' });
      // recargar configuración del programa
      const programaId = configToDelete.programa_id;
      await loadConfiguracion(programaId);
    } catch (e: any) {
      const msg = e?.message || 'Error al eliminar configuración';
      enqueueSnackbar(msg, { variant: 'error' });
    } finally {
      setDeleteConfigLoading(false);
      setConfigToDelete(null);
    }
  };

  const handleConfigSaved = async () => {
    if (!selectedPrograma) return;
    await loadConfiguracion(selectedPrograma.programa_id);
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

      {/* Sección de Configuración de Programas */}
      <div className="bg-white rounded-xl p-6 shadow border">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Settings className="w-5 h-5" />
              Configuración de Programas
            </h2>
            <p className="text-sm text-gray-500 mt-1">{programas.length} programas disponibles</p>
          </div>
        </div>

        {programasLoading && <div className="text-center text-gray-600">Cargando programas...</div>}
        {programasError && <div className="text-center text-red-600">{programasError}</div>}

        {!programasLoading && !programasError && (
          <div className="space-y-3">
            {programas.map((programa) => {
              const config = configuraciones.get(programa.programa_id);
              const isLoading = configLoadingMap.get(programa.programa_id) ?? false;

              return (
                <div
                  key={programa.programa_id}
                  className="flex items-center gap-4 p-4 border rounded-lg hover:shadow-sm transition bg-gray-50"
                >
                  <div className="w-12 h-12 bg-blue-900 text-white rounded-full flex items-center justify-center flex-shrink-0">
                    <Settings className="w-5 h-5" />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-gray-800">{programa.nombre_programa}</div>
                    
                    {isLoading ? (
                      <div className="text-xs text-gray-500 mt-1">Cargando configuración...</div>
                    ) : config ? (
                      <div className="text-xs text-gray-600 mt-1 space-y-0.5">
                        <div>Nota aprobatoria: <span className="font-semibold">{config.nota_aprobatoria}</span></div>
                        <div>Semestre límite: <span className="font-semibold">{config.semestre_limite_electivas}</span></div>
                      </div>
                    ) : (
                      <div className="text-xs text-orange-600 mt-1 font-medium">Sin configuración</div>
                    )}
                  </div>

                  <div className="flex items-center gap-2 flex-shrink-0">
                    <button
                      onClick={() => loadConfiguracion(programa.programa_id)}
                      disabled={isLoading}
                      className="px-3 py-1 text-sm rounded-md bg-gray-300 text-gray-700 hover:bg-gray-400 disabled:opacity-50"
                    >
                      {isLoading ? 'Cargando...' : 'Recargar'}
                    </button>

                    <button
                      onClick={() => handleEditConfig(programa)}
                      disabled={isLoading}
                      className="px-3 py-1.5 text-sm rounded-md bg-blue-900 text-white hover:bg-blue-800 disabled:opacity-50 flex items-center gap-1"
                    >
                      <Edit2 className="w-4 h-4" />
                      {config ? 'Editar' : 'Crear'}
                    </button>

                    {config && (
                      <button
                        onClick={() => handleDeleteConfig(config)}
                        disabled={isLoading}
                        className="px-3 py-1.5 text-sm rounded-md bg-red-600 text-white hover:bg-red-700 disabled:opacity-50 flex items-center gap-1"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
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

      <ConfiguracionFormDialog
        isOpen={showConfigDialog}
        onClose={() => {
          setShowConfigDialog(false);
          setSelectedPrograma(null);
          setSelectedConfig(null);
        }}
        onSaved={handleConfigSaved}
        configuracion={selectedConfig}
        programaId={selectedPrograma?.programa_id ?? 0}
        programaNombre={selectedPrograma?.nombre_programa ?? ''}
      />

      <ConfirmDialog
        isOpen={showConfirmDeleteConfig}
        title="Eliminar configuración"
        description={configToDelete ? `¿Eliminar configuración de ${configToDelete.programa_nombre}?` : 'Eliminar configuración?'}
        confirmLabel="Eliminar"
        cancelLabel="Cancelar"
        loading={deleteConfigLoading}
        onConfirm={onConfirmDeleteConfig}
        onCancel={() => {
          setShowConfirmDeleteConfig(false);
          setConfigToDelete(null);
        }}
      />
    </div>
  );
}