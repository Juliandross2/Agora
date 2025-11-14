import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from './DashboardLayout';
import Login from './pages/Login';
import Home from './pages/Home';
import Config from './pages/Config';
import Comparacion from './pages/Comparacion';
import ComparacionList from './pages/ComparacionList';
import ComparacionDetailView from './pages/ComparacionDetailView';
import GestionProgramas from './pages/GestionProgramas';
import PensumActual from './pages/PensumActual';
import GestionElectivas from './pages/GestionElectivas';
import { getToken, isTokenValid } from './services/consumers/Auth';

const RequireAuth = ({ children }) => {
  const token = getToken();
  // usa isTokenValid si la tienes; si no, déjalo como token != null
  if (!token || (typeof isTokenValid === 'function' && !isTokenValid(token))) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const RedirectIfAuth = ({ children }) => {
  const token = getToken();
  return token ? <Navigate to="/home" replace /> : children;
};

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rutas públicas */}
        <Route path="/login" element={<RedirectIfAuth><Login /></RedirectIfAuth>} />

        {/* Layout protegido: DashboardLayout se monta UNA sola vez */}
        <Route
          element={
            <RequireAuth>
              <DashboardLayout />
            </RequireAuth>
          }
        >
           {/* /home protegido */}
          <Route path="/home" element={<RequireAuth><Home /></RequireAuth>} />

          {/* config protegido */}
          <Route path="/config" element={<RequireAuth><Config /></RequireAuth>} />

          {/* gestión de programas protegido */}
          <Route path="/gestion-programas" element={<RequireAuth><GestionProgramas /></RequireAuth>} />
          {/* Pensum actual de programa **/}
          <Route path="/pensum/:programaId" element={<PensumActual />} />

          {/**Gestion de electivas */}
          <Route path="/gestion-electivas" element={<RequireAuth><GestionElectivas /></RequireAuth>} />
          <Route path="/gestion-electivas/:programaId" element={<RequireAuth><GestionElectivas /></RequireAuth>} />
          {/* comparacion protegido */}
          <Route path="/comparacion" element={<RequireAuth><Comparacion /></RequireAuth>} />
          <Route path="/comparacion-resultados" element={<RequireAuth><ComparacionList /></RequireAuth>} />
          <Route path="/comparacion-detalle/:estudianteId" element={<RequireAuth><ComparacionDetailView /></RequireAuth>} />
        </Route>

        {/* fallback */}
        <Route path="*" element={<Navigate to="/home" replace />} />
      </Routes>
    </BrowserRouter>
  );
}