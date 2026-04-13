import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import LoginPage from './pages/Login/LoginPage'
import AlumnosPage from './pages/Alumnos/AlumnosPage'
import ClasesPage from './pages/Clases/ClasesPage'
import AsistenciaPage from './pages/Clases/AsistenciaPage'
import PagoClasePage from './pages/Pagos/PagoClasePage'
import PagoMensualPage from './pages/Pagos/PagoMensualPage'
import ImpagarPage from './pages/Reportes/ImpagarPage'
import ReportePage from './pages/Reportes/ReportePage'
import UsuariosPage from './pages/Admin/UsuariosPage'
import AuditoriaPage from './pages/Admin/AuditoriaPage'

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token')
  if (!token) return <Navigate to="/login" replace />
  return (
    <>
      <Navbar />
      <div className="container-fluid py-3 px-4">{children}</div>
    </>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/alumnos" element={<ProtectedRoute><AlumnosPage /></ProtectedRoute>} />
        <Route path="/clases" element={<ProtectedRoute><ClasesPage /></ProtectedRoute>} />
        <Route path="/clases/:id/asistencia" element={<ProtectedRoute><AsistenciaPage /></ProtectedRoute>} />
        <Route path="/pagos/clase" element={<ProtectedRoute><PagoClasePage /></ProtectedRoute>} />
        <Route path="/pagos/mensual" element={<ProtectedRoute><PagoMensualPage /></ProtectedRoute>} />
        <Route path="/reportes/impagas" element={<ProtectedRoute><ImpagarPage /></ProtectedRoute>} />
        <Route path="/reportes/pagos" element={<ProtectedRoute><ReportePage /></ProtectedRoute>} />
        <Route path="/admin/usuarios" element={<ProtectedRoute><UsuariosPage /></ProtectedRoute>} />
        <Route path="/admin/auditoria" element={<ProtectedRoute><AuditoriaPage /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/alumnos" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
