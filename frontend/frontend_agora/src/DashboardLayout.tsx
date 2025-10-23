import React, { useState } from 'react';
import Sidebar from './components/Sidebar';

interface DashboardLayoutProps {
  // children as render-prop: recibe el activeSection y devuelve contenido derecho
  children: (activeSection: string) => React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const [activeSection, setActiveSection] = useState('home');
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar
        activeSection={activeSection}
        setActiveSection={setActiveSection}
        isCollapsed={isCollapsed}
        onToggle={() => setIsCollapsed((s) => !s)}
      />
      <main className="flex-1 overflow-auto p-6 transition-all">
        {/* Renderizamos el contenido derecho según activeSection */}
        {children(activeSection)}
      </main>
    </div>
  );
};

export default DashboardLayout;
