import { useState, useEffect } from 'react'
import { getAlumnos } from '../../api/alumnos'
import { getClases } from '../../api/clases'
import { registerPagoClase } from '../../api/pagos'
import AlertMessage from '../../components/AlertMessage'
import LoadingSpinner from '../../components/LoadingSpinner'

function formatDate(d) {
  if (!d) return ''
  const [y, m, day] = d.split('-')
  return `${day}/${m}/${y}`
}

export default function PagoClasePage() {
  const [alumnos, setAlumnos] = useState([])
  const [clases, setClases] = useState([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState({ alumno_id: '', clase_id: '', monto: '', fecha_pago: '' })
  const [alert, setAlert] = useState({ type: 'success', msg: '' })
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    Promise.all([getAlumnos(), getClases()])
      .then(([a, c]) => { setAlumnos(a); setClases(c) })
      .catch(() => setAlert({ type: 'danger', msg: 'Error al cargar datos' }))
      .finally(() => setLoading(false))
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setAlert({ type: 'success', msg: '' })
    try {
      const result = await registerPagoClase({
        alumno_id: Number(form.alumno_id),
        clase_id: Number(form.clase_id),
        monto: Number(form.monto),
        fecha_pago: form.fecha_pago,
      })
      if (result.warning) {
        setAlert({ type: 'warning', msg: `Pago registrado. Aviso: ${result.warning}` })
      } else {
        setAlert({ type: 'success', msg: 'Pago por clase registrado correctamente' })
      }
      setForm({ alumno_id: '', clase_id: '', monto: '', fecha_pago: '' })
    } catch (err) {
      setAlert({ type: 'danger', msg: err.response?.data?.detail || 'Error al registrar pago' })
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div style={{ maxWidth: 500 }}>
      <h4 className="mb-3">Pago por Clase</h4>
      <AlertMessage type={alert.type} message={alert.msg} onClose={() => setAlert({ ...alert, msg: '' })} />
      <form onSubmit={handleSubmit} className="card p-3">
        <div className="mb-3">
          <label className="form-label">Alumno *</label>
          <select className="form-select" value={form.alumno_id}
            onChange={(e) => setForm({ ...form, alumno_id: e.target.value })} required>
            <option value="">Seleccionar...</option>
            {alumnos.map((a) => (
              <option key={a.id} value={a.id}>{a.apellido}, {a.nombre}</option>
            ))}
          </select>
        </div>
        <div className="mb-3">
          <label className="form-label">Clase *</label>
          <select className="form-select" value={form.clase_id}
            onChange={(e) => setForm({ ...form, clase_id: e.target.value })} required>
            <option value="">Seleccionar...</option>
            {clases.map((c) => (
              <option key={c.id} value={c.id}>{formatDate(c.fecha)} — {c.estado}</option>
            ))}
          </select>
        </div>
        <div className="mb-3">
          <label className="form-label">Monto *</label>
          <input type="number" step="0.01" min="0.01" className="form-control"
            value={form.monto} onChange={(e) => setForm({ ...form, monto: e.target.value })} required />
        </div>
        <div className="mb-3">
          <label className="form-label">Fecha de pago *</label>
          <input type="date" className="form-control"
            value={form.fecha_pago} onChange={(e) => setForm({ ...form, fecha_pago: e.target.value })} required />
        </div>
        <button type="submit" className="btn btn-primary w-100" disabled={saving}>
          {saving ? 'Registrando...' : 'Registrar pago'}
        </button>
      </form>
    </div>
  )
}
