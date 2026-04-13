import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <Link className="navbar-brand fw-bold" to="/alumnos">⚡ KickManager</Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navMenu"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="navMenu">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <Link className="nav-link" to="/alumnos">Alumnos</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/clases">Clases</Link>
            </li>
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                Pagos
              </a>
              <ul className="dropdown-menu">
                <li><Link className="dropdown-item" to="/pagos/clase">Pago por Clase</Link></li>
                <li><Link className="dropdown-item" to="/pagos/mensual">Pago Mensual</Link></li>
              </ul>
            </li>
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                Reportes
              </a>
              <ul className="dropdown-menu">
                <li><Link className="dropdown-item" to="/reportes/impagas">Clases Impagas</Link></li>
                <li><Link className="dropdown-item" to="/reportes/pagos">Reporte de Pagos</Link></li>
              </ul>
            </li>
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                Admin
              </a>
              <ul className="dropdown-menu">
                <li><Link className="dropdown-item" to="/admin/usuarios">Usuarios</Link></li>
                <li><Link className="dropdown-item" to="/admin/auditoria">Auditoría</Link></li>
              </ul>
            </li>
          </ul>
          <div className="d-flex align-items-center gap-3">
            {user && <span className="text-light small">{user.username}</span>}
            <button className="btn btn-outline-light btn-sm" onClick={logout}>Cerrar sesión</button>
          </div>
        </div>
      </div>
    </nav>
  )
}
