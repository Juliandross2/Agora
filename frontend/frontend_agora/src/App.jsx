import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import { getToken } from './services/consumers/Auth';

const RequireAuth = ({ children }) => {
  const token = getToken();
  return token ? children : <Navigate to="/login" replace />;
};

const RedirectIfAuth = ({ children }) => {
  const token = getToken();
  return token ? <Navigate to="/home" replace /> : children;
};

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* raíz decide según token */}
        <Route path="/" element={<Navigate to={getToken() ? '/home' : '/login'} replace />} />

        {/* /login redirige al home si ya hay token */}
        <Route path="/login" element={<RedirectIfAuth><Login /></RedirectIfAuth>} />

        {/* /home protegido */}
        <Route path="/home" element={<RequireAuth><Home /></RequireAuth>} />

        {/* rutas adicionales protegidas pueden usar RequireAuth */}
      </Routes>
    </BrowserRouter>
  );
}