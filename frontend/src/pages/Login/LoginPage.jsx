import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../../api/client'
import AlertMessage from '../../components/AlertMessage'

export default function LoginPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const { data } = await client.post('/auth/login', form)
      localStorage.setItem('token', data.access_token)
      // Decode token payload to get user info
      const payload = JSON.parse(atob(data.access_token.split('.')[1]))
      localStorage.setItem('user', JSON.stringify({ id: payload.sub, username: form.username }))
      navigate('/alumnos')
    } catch (err) {
      setError(err.response?.status === 401 ? 'Usuario o contraseña incorrectos' : 'Error de conexión')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center bg-light">
      <div className="card shadow" style={{ width: '100%', maxWidth: 400 }}>
        <div className="card-body p-4">
          <h4 className="card-title text-center mb-4 fw-bold">⚡ KickManager</h4>
          <AlertMessage message={error} onClose={() => setError('')} />
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label">Usuario</label>
              <input
                className="form-control"
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
                required
                autoFocus
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Contraseña</label>
              <input
                type="password"
                className="form-control"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                required
              />
            </div>
            <button className="btn btn-primary w-100" disabled={loading}>
              {loading ? 'Ingresando...' : 'Ingresar'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
