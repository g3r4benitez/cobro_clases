import { useState } from 'react'
import client from '../../api/client'
import AlertMessage from '../../components/AlertMessage'

export default function UsuariosPage() {
  const [form, setForm] = useState({ username: '', password: '' })
  const [alert, setAlert] = useState({ type: 'success', msg: '' })
  const [saving, setSaving] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setAlert({ type: 'success', msg: '' })
    try {
      await client.post('/usuarios', form)
      setAlert({ type: 'success', msg: `Usuario "${form.username}" creado correctamente` })
      setForm({ username: '', password: '' })
    } catch (err) {
      const detail = err.response?.data?.detail
      const type = err.response?.status === 409 ? 'warning' : 'danger'
      setAlert({ type, msg: typeof detail === 'string' ? detail : 'Error al crear usuario' })
    } finally {
      setSaving(false)
    }
  }

  return (
    <div style={{ maxWidth: 450 }}>
      <h4 className="mb-3">Gestión de Usuarios</h4>
      <AlertMessage type={alert.type} message={alert.msg} onClose={() => setAlert({ ...alert, msg: '' })} />
      <form onSubmit={handleSubmit} className="card p-3">
        <h6 className="mb-3">Nuevo usuario del sistema</h6>
        <div className="mb-3">
          <label className="form-label">Nombre de usuario *</label>
          <input className="form-control" value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            placeholder="mín. 3 caracteres, sin espacios" required />
        </div>
        <div className="mb-3">
          <label className="form-label">Contraseña *</label>
          <input type="password" className="form-control" value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            placeholder="mín. 6 caracteres" required />
        </div>
        <button type="submit" className="btn btn-primary w-100" disabled={saving}>
          {saving ? 'Creando...' : 'Crear usuario'}
        </button>
      </form>
    </div>
  )
}
