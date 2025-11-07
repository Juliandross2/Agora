import React, { createContext, useContext, useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './components/Sidebar';

type ActiveSectionCtx = {
  activeSection: string;
  setActiveSection: (s: string) => void;
};

const ActiveSectionContext = createContext<ActiveSectionCtx>({
  activeSection: 'home',
  setActiveSection: () => {},
});

export const useActiveSection = () => useContext(ActiveSectionContext);

export default function DashboardLayout() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [activeSection, setActiveSection] = useState('home');

  return (
    <ActiveSectionContext.Provider value={{ activeSection, setActiveSection }}>
      <div className="flex h-screen">
        <Sidebar
          activeSection={activeSection}
          setActiveSection={setActiveSection}
          isCollapsed={isCollapsed}
          onToggle={() => setIsCollapsed(v => !v)}
        />
        <main className="flex-1 overflow-auto bg-gray-50">
          <Outlet />
        </main>
      </div>
    </ActiveSectionContext.Provider>
  );
}
