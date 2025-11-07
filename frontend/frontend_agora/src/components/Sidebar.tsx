import React, { useEffect, useState } from "react";
import {
  BookOpen,
  Users,
  Settings,
  ArrowLeft,
  User,
  LogOut,
  HomeIcon,
} from "lucide-react";
import { useNavigate } from "react-router-dom"; // <-- agregado
import { getProfile } from "../services/consumers/UsuarioClient";
import { clearToken } from "../services/consumers/Auth"; // <-- import agregado
import type { User as Usuario } from "../services/domain/UsuarioModels";

interface SidebarProps {
  activeSection: string;
  setActiveSection: (section: string) => void;
  isCollapsed: boolean;
  onToggle: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  activeSection,
  setActiveSection,
  isCollapsed,
  onToggle,
}) => {
  const [profile, setProfile] = useState<Usuario | null>(null);
  const [profileLoading, setProfileLoading] = useState(false);
  const navigate = useNavigate(); // <-- agregado

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
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <aside
      /* animación de ancho y overflow para evitar parpadeos; duración más suave */
      className={`bg-gradient-to-b from-blue-900 to-blue-800 text-white flex flex-col transition-[width] duration-500 ease-in-out overflow-hidden ${isCollapsed ? "w-28" : "w-80"}`}
      aria-hidden={false}
    >
      <div className="p-4 border-b border-blue-700">
        <div
          className={`flex items-center ${
            isCollapsed ? "justify-center" : "justify-start"
          } gap-3`}
        >
          <a
            href="https://www.unicauca.edu.co"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-4 px-2 py-1 rounded hover:bg-white/5 transition"
          >
            <img
              src="/unicauca_logo.svg"
              alt="Universidad del Cauca"
              /* transicion de tamaño y opacidad para que reduzca suavemente */
              className={`w-auto object-contain transition-all duration-500 ${isCollapsed ? "h-10 opacity-80" : "h-16 opacity-100"}`}
            />

            {/* separador blanco vertical visible solo cuando no está colapsado */}
            {!isCollapsed && (
              <div className="h-10 w-px bg-white/50" aria-hidden="true" />
            )}

            {/* animación de texto: usamos max-w + opacity para transición suave */}
            <div
              className={`overflow-hidden transition-all duration-300 ease-in-out ${
                isCollapsed ? "max-w-0 opacity-0" : "max-w-[220px] opacity-100"
              }`}
              aria-hidden={isCollapsed}
            >
              {!isCollapsed && (
                <div className="text-lg font-bold text-white leading-none select-none">
                  Sistema AGORA
                </div>
              )}
            </div>
          </a>
        </div>
      </div>

      <div className="p-4 border-b border-blue-700">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-orange-400 rounded-full flex items-center justify-center">
            <User size={isCollapsed ? 18 : 32} />
          </div>

          {/* info de usuario con animación de opacidad y max-width */}
          <div className={`flex-1 transition-all duration-300 ease-in-out ${isCollapsed ? "max-w-0 opacity-0" : "max-w-full opacity-100"}`}>
            {/* mostrar nombre desde perfil si está disponible */}
            <h3 className="text-lg font-semibold">
              {profileLoading ? "Cargando..." : profile?.nombre_usuario ?? "Carlos Ardila"}
            </h3>
            <p className="text-blue-200 text-sm">
              {profile ? profile.email_usuario : "Coordinador de electivas"}
            </p>
          </div>

          <button
            onClick={onToggle}
            className="w-10 h-10 rounded-full border-2 border-white flex items-center justify-center hover:bg-blue-700 transition-transform duration-300"
            aria-label={isCollapsed ? "Expandir sidebar" : "Minimizar sidebar"}
            title={isCollapsed ? "Expandir" : "Minimizar"}
          >
            <ArrowLeft size={18} className={`transition-transform duration-300 ${isCollapsed ? "rotate-180" : "rotate-0"}`} />
          </button>
        </div>
      </div>

      <nav className="flex-1 p-3 space-y-2">
        <button
          onClick={() => {
            setActiveSection("home");
            navigate('/home');
          }}
          className={`w-full flex items-center gap-4 px-3 py-3 rounded-lg transition-colors duration-200 ${
            activeSection === "home" ? "bg-blue-700" : "hover:bg-blue-700"
          }`}
        >
          <HomeIcon size={20} />
          <span className={`overflow-hidden transition-all duration-300 ${isCollapsed ? "max-w-0 opacity-0" : "max-w-[140px] opacity-100"} text-lg font-medium`}>
            Home
          </span>
        </button>

        <button
          onClick={() => {
            setActiveSection("programas");
            navigate("/gestion-programas");
          }}
          className={`w-full flex items-center gap-4 px-3 py-3 rounded-lg transition-colors duration-200 ${
            activeSection === "programas" ? "bg-blue-700" : "hover:bg-blue-700"
          }`}
        >
          <BookOpen size={20} />
          <span className={`overflow-hidden transition-all duration-300 ${isCollapsed ? "max-w-0 opacity-0" : "max-w-[140px] opacity-100"} text-lg font-medium`}>
            Programas
          </span>
        </button>

        <button
          onClick={() => {
            setActiveSection("comparacion");
            navigate("/comparacion");
          }}
          className={`w-full flex items-center gap-4 px-3 py-3 rounded-lg transition-colors duration-200 ${
            activeSection === "comparacion" ? "bg-blue-700" : "hover:bg-blue-700"
          }`}
        >
          <Users size={20} />
          <span className={`overflow-hidden text-start transition-all duration-300 ${isCollapsed ? "max-w-0 opacity-0" : "max-w-[140px] opacity-100"} text-lg font-medium`}>
            Comparación de pensum
          </span>
        </button>

        <button
          onClick={() => {
            setActiveSection("configuracion");
            navigate("/config"); // navegar a la ruta de configuración
          }}
          className={`w-full flex items-center gap-4 px-3 py-3 rounded-lg transition-colors duration-200 ${
            activeSection === "configuracion" ? "bg-blue-700" : "hover:bg-blue-700"
          }`}
        >
          <Settings size={20} />
          <span className={`overflow-hidden transition-all duration-300 ${isCollapsed ? "max-w-0 opacity-0" : "max-w-[140px] opacity-100"} text-lg font-medium`}>
            Configuración
          </span>
        </button>
      </nav>

      {/* footer: logout ocupa todo el ancho y se pega al fondo */}
      <div className="mt-auto w-full p-3 border-t border-blue-700">
        <button
          onClick={() => {
            clearToken(); // elimina el token correctamente
            window.location.href = "/login";
          }}
          className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-md bg-red-600 hover:bg-red-700 transition text-white"
          aria-label="Cerrar sesión"
          title="Cerrar sesión"
        >
          <LogOut size={18} />
          <span className={`ml-2 text-sm font-medium overflow-hidden transition-all duration-300 ${isCollapsed ? "max-w-0 opacity-0" : "max-w-[120px] opacity-100"}`}>
            {!isCollapsed && "Cerrar sesión"}
          </span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
