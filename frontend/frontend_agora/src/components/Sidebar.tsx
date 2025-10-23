import React, { useEffect, useState } from 'react';
import { BookOpen, Users, Settings, ArrowLeft, User, LogOut, HomeIcon } from 'lucide-react';
import { getProfile } from '../services/consumers/UsuarioClient';
import { clearToken } from '../services/consumers/Auth'; // <-- import agregado
import type { User as Usuario } from '../services/domain/UsuarioModels';

interface SidebarProps {
  activeSection: string;
  setActiveSection: (section: string) => void;
  isCollapsed: boolean;
  onToggle: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeSection, setActiveSection, isCollapsed, onToggle }) => {
  const [profile, setProfile] = useState<Usuario | null>(null);
  const [profileLoading, setProfileLoading] = useState(false);

  useEffect(() => {
    let mounted = true;
    const loadProfile = async () => {
      setProfileLoading(true);
      try {
        const res = await getProfile();
        if (!mounted) return;
        setProfile(res.user ?? null);
      } catch (e) {
        // Silenciar errores de perfil (por ejemplo al probar sin token)
        setProfile(null);
      } finally {
        if (mounted) setProfileLoading(false);
      }
    };
    loadProfile();
    return () => { mounted = false; };
  }, []);

  return (
    <aside
      className={`bg-gradient-to-b from-blue-900 to-blue-800 text-white flex flex-col transition-all duration-300 ${
        isCollapsed ? 'w-20' : 'w-80'
      }`}
      aria-hidden={false}
    >
      <div className="p-4 border-b border-blue-700">
        <div className={`flex items-center ${isCollapsed ? 'justify-center' : 'justify-start'} gap-3`}>
          <a
            href="https://www.unicauca.edu.co"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-4 px-2 py-1 rounded hover:bg-white/5 transition"
          >
            <img
              src="/unicauca_logo.svg"
              alt="Universidad del Cauca"
              className={`${isCollapsed ? 'h-10' : 'h-16'} w-auto object-contain`}
            />

            {/* separador blanco vertical visible solo cuando no está colapsado */}
            {!isCollapsed && <div className="h-10 w-px bg-white/50" aria-hidden="true" />}

            {!isCollapsed && (
              <div className="text-lg font-bold text-white leading-none select-none">
                Sistema AGORA
              </div>
            )}
          </a>
        </div>
      </div>

      <div className="p-4 border-b border-blue-700">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-orange-400 rounded-full flex items-center justify-center">
            <User size={isCollapsed ? 18 : 32} />
          </div>

          {!isCollapsed ? (
            <div className="flex-1">
              {/* mostrar nombre desde perfil si está disponible */}
              <h3 className="text-lg font-semibold">
                {profileLoading ? 'Cargando...' : (profile?.nombre_usuario ?? 'Carlos Ardila')}
              </h3>
              <p className="text-blue-200 text-sm">
                {profile ? profile.email_usuario : 'Coordinador de electivas'}
              </p>
            </div>
          ) : null}

          <button
            onClick={onToggle}
            className="w-10 h-10 rounded-full border-2 border-white flex items-center justify-center hover:bg-blue-700 transition"
            aria-label={isCollapsed ? 'Expandir sidebar' : 'Minimizar sidebar'}
            title={isCollapsed ? 'Expandir' : 'Minimizar'}
          >
            <ArrowLeft size={18} className={`${isCollapsed ? 'rotate-180' : ''} transition-transform`} />
          </button>
        </div>
      </div>

      <nav className="flex-1 p-3 space-y-2">
        <button
          onClick={() => setActiveSection('home')}
          className={`w-full flex items-center gap-4 px-3 py-3 rounded-lg transition ${
            activeSection === 'home' ? 'bg-blue-700' : 'hover:bg-blue-700'
          }`}
        >
          <HomeIcon size={20} />
          <span className={`${isCollapsed ? 'hidden' : 'block'} text-lg font-medium`}>Home</span>
        </button>

        <button
          onClick={() => setActiveSection('programas')}
          className={`w-full flex items-center gap-4 px-3 py-3 rounded-lg transition ${
            activeSection === 'programas' ? 'bg-blue-700' : 'hover:bg-blue-700'
          }`}
        >
          <BookOpen size={20} />
          <span className={`${isCollapsed ? 'hidden' : 'block'} text-lg font-medium`}>Programas</span>
        </button>
        
        <button
          onClick={() => setActiveSection('comparacion')}
          className={`w-full flex items-center gap-4 px-3 py-3 rounded-lg transition ${
            activeSection === 'comparacion' ? 'bg-blue-700' : 'hover:bg-blue-700'
          }`}
        >
          <Users size={20} />
          <span className={`${isCollapsed ? 'hidden' : 'block'} text-lg font-medium`}>Comparación pensum</span>
        </button>

        <button
          onClick={() => setActiveSection('configuracion')}
          className={`w-full flex items-center gap-4 px-3 py-3 rounded-lg transition ${
            activeSection === 'configuracion' ? 'bg-blue-700' : 'hover:bg-blue-700'
          }`}
        >
          <Settings size={20} />
          <span className={`${isCollapsed ? 'hidden' : 'block'} text-lg font-medium`}>Configuración</span>
        </button>
      </nav>

      {/* footer: logout ocupa todo el ancho y se pega al fondo */}
      <div className="mt-auto w-full p-3 border-t border-blue-700">
        <button
          onClick={() => {
            clearToken(); // elimina el token correctamente
            window.location.href = '/login';
          }}
          className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-md bg-red-600 hover:bg-red-700 transition text-white"
          aria-label="Cerrar sesión"
          title="Cerrar sesión"
        >
          <LogOut size={18} />
          {!isCollapsed && <span className="ml-2 text-sm font-medium">Cerrar sesión</span>}
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;