import React from 'react';
import { BookOpen, Users, Settings, ArrowLeft, User } from 'lucide-react';

interface SidebarProps {
  activeSection: string;
  setActiveSection: (section: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeSection, setActiveSection }) => {
  return (
    <aside className="w-80 bg-gradient-to-b from-blue-900 to-blue-800 text-white flex flex-col">
      <div className="p-6 border-b border-blue-700">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-white rounded-lg flex items-center justify-center">
            <div className="text-blue-900 font-bold text-xs text-center">
              <div>Universidad</div>
              <div>del Cauca</div>
            </div>
          </div>
          <div>
            <div className="text-xl font-bold">Sistema AGORA</div>
          </div>
        </div>
      </div>

      <div className="p-6 border-b border-blue-700">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-orange-400 rounded-full flex items-center justify-center">
            <User size={32} />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold">Carlos Ardila</h3>
            <p className="text-blue-200 text-sm">Coordinador de electivas</p>
          </div>
          <button className="w-10 h-10 rounded-full border-2 border-white flex items-center justify-center hover:bg-blue-700 transition">
            <ArrowLeft size={20} />
          </button>
        </div>
      </div>

      <nav className="flex-1 p-4">
        <button
          onClick={() => setActiveSection('programas')}
          className={`w-full flex items-center gap-4 px-6 py-4 rounded-lg transition mb-2 ${
            activeSection === 'programas' ? 'bg-blue-700' : 'hover:bg-blue-700'
          }`}
        >
          <BookOpen size={24} />
          <span className="text-lg font-medium">Programas</span>
        </button>

        <button
          onClick={() => setActiveSection('comparacion')}
          className={`w-full flex items-center gap-4 px-6 py-4 rounded-lg transition mb-2 ${
            activeSection === 'comparacion' ? 'bg-blue-700' : 'hover:bg-blue-700'
          }`}
        >
          <Users size={24} />
          <span className="text-lg font-medium">Comparación pensum</span>
        </button>

        <button
          onClick={() => setActiveSection('configuracion')}
          className={`w-full flex items-center gap-4 px-6 py-4 rounded-lg transition ${
            activeSection === 'configuracion' ? 'bg-blue-700' : 'hover:bg-blue-700'
          }`}
        >
          <Settings size={24} />
          <span className="text-lg font-medium">Configuración</span>
        </button>
      </nav>
    </aside>
  );
};

export default Sidebar;