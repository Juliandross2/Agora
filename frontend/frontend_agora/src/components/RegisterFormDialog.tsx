import React, { useState } from 'react';
import { Eye, EyeOff, X, UserPlus } from 'lucide-react';
import { useSnackbar } from 'notistack';
import { registerUser, listarUsuarios } from '../services/consumers/UsuarioClient';
import type { User } from '../services/domain/UsuarioModels';

interface RegisterFormDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onUserRegistered: (users: User[]) => void;
}

interface FieldErrors {
  nombre_usuario?: string;
  email_usuario?: string;
  contrasenia?: string;
  confirmar_contrasenia?: string;
}

export default function RegisterFormDialog({ isOpen, onClose, onUserRegistered }: RegisterFormDialogProps) {
  const { enqueueSnackbar } = useSnackbar();
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});

  const resetForm = () => {
    setNombre('');
    setEmail('');
    setPassword('');
    setConfirm('');
    setShowPassword(false);
    setShowConfirm(false);
    setFieldErrors({});
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFieldErrors({});

    if (!nombre || !email || !password || !confirm) {
      enqueueSnackbar('Completa todos los campos', { variant: 'warning' });
      return;
    }
    if (password !== confirm) {
      enqueueSnackbar('Las contraseñas no coinciden', { variant: 'warning' });
      return;
    }

    setLoading(true);
    try {
      const payload = {
        nombre_usuario: nombre,
        email_usuario: email,
        contrasenia: password,
        confirmar_contrasenia: confirm
      };
      const res = await registerUser(payload);
      enqueueSnackbar(res.message || 'Usuario registrado exitosamente', { variant: 'success' });
      
      // Refrescar lista de usuarios
      const list = await listarUsuarios();
      onUserRegistered(list);
      
      handleClose();
    } catch (e: any) {
      // Manejar errores específicos de validación
      if (e?.response?.data?.details) {
        const details = e.response.data.details;
        setFieldErrors(details);
        
        // Mostrar mensaje general del error
        const generalMsg = e.response.data.error || 'Error de validación';
        enqueueSnackbar(generalMsg, { variant: 'error' });
      } else if (e?.details) {
        // Si el error viene directamente con details
        setFieldErrors(e.details);
        enqueueSnackbar(e?.error || 'Error de validación', { variant: 'error' });
      } else {
        // Error genérico
        const msg = e?.message || 'Error registrando usuario';
        enqueueSnackbar(msg, { variant: 'error' });
      }
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-md mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <UserPlus className="w-5 h-5 text-blue-900" />
            Registrar Administrador
          </h2>
          <button
            onClick={handleClose}
            className="p-1 hover:bg-gray-100 rounded-full transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nombre completo
            </label>
            <input
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              className={`w-full rounded-md border px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none ${
                fieldErrors.nombre_usuario ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Ingresa el nombre completo"
              required
            />
            {fieldErrors.nombre_usuario && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.nombre_usuario}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Correo electrónico
            </label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              type="email"
              className={`w-full rounded-md border px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none ${
                fieldErrors.email_usuario ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="ejemplo@unicauca.edu.co"
              required
            />
            {fieldErrors.email_usuario && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.email_usuario}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Contraseña
            </label>
            <div className="relative">
              <input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type={showPassword ? 'text' : 'password'}
                className={`w-full rounded-md border px-3 py-2 pr-10 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none ${
                  fieldErrors.contrasenia ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Ingresa una contraseña segura"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
            {fieldErrors.contrasenia && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.contrasenia}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Confirmar contraseña
            </label>
            <div className="relative">
              <input
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                type={showConfirm ? 'text' : 'password'}
                className={`w-full rounded-md border px-3 py-2 pr-10 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none ${
                  fieldErrors.confirmar_contrasenia ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Confirma la contraseña"
                required
              />
              <button
                type="button"
                onClick={() => setShowConfirm(!showConfirm)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showConfirm ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
            {fieldErrors.confirmar_contrasenia && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.confirmar_contrasenia}</p>
            )}
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={handleClose}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-blue-900 text-white rounded-md hover:bg-blue-800 disabled:opacity-60 transition flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Registrando...
                </>
              ) : (
                <>
                  <UserPlus className="w-4 h-4" />
                  Registrar
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}