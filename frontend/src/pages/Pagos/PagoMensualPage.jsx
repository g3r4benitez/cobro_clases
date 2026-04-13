import { useState, useEffect } from 'react'
import { getAlumnos } from '../../api/alumnos'
import { registerPagoMensual } from '../../api/pagos'
import AlertMessage from '../../components/AlertMessage'
import LoadingSpinner from '../../components/LoadingSpinner'

const MESES = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre',
]

export default function PagoMensualPage() {
  const [alumnos, setAlumnos] = useState([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState({
    alumno_id: '', mes_cubierto: '', anio_cubierto: new Date().getFullYear(), fecha_pago: '', monto: '',
  })
  const [alert, setAlert] = useState({ type: 'success', msg: '' })
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    getAlumnos()
      .then(setAlumnos)
      .catch(() => setAlert({ type: 'danger', msg: 'Error al cargar alumnos' }))
      .finally(() => setLoading(false))
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setAlert({ type: 'success', msg: '' })
    try {
      await registerPagoMensual({
        alumno_id: Number(form.alumno_id),
        mes_cubierto: Number(form.mes_cubierto),
        anio_cubierto: Number(form.anio_cubierto),
        fecha_pago: form.fecha_pago,
        monto: Number(form.monto),
      })
      setAlert({ type: 'success', msg: 'Pago mensual registrado correctamente' })
      setForm({ alumno_id: '', mes_cubierto: '', anio_cubierto: new Date().getFullYear(), fecha_pago: '', monto: '' })
    } catch (err) {
      const detail = err.response?.data?.detail
      const type = err.response?.status === 409 ? 'warning' : 'danger'
      setAlert({ type, msg: typeof detail === 'string' ? detail : 'Error al registrar pago' })
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div style={{ maxWidth: 500 }}>
      <h4 className="mb-3">Pago Mensual</h4>
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
        <div className="row g-2 mb-3">
          <div className="col">
            <label className="form-label">Mes cubierto *</label>
            <select className="form-select" value={form.mes_cubierto}
              onChange={(e) => setForm({ ...form, mes_cubierto: e.target.value })} required>
              <option value="">Mes...</option>
              {MESES.map((m, i) => (
                <option key={i + 1} value={i + 1}>{m}</option>
              ))}
            </select>
          </div>
          <div className="col">
            <label className="form-label">Año *</label>
            <input type="number" className="form-control" min="2001"
              value={form.anio_cubierto}
              onChange={(e) => setForm({ ...form, anio_cubierto: e.target.value })} required />
          </div>
        </div>
        <div className="mb-3">
          <label className="form-label">Fecha de pago *</label>
          <input type="date" className="form-control" value={form.fecha_pago}
            onChange={(e) => setForm({ ...form, fecha_pago: e.target.value })} required />
        </div>
        <div className="mb-3">
          <label className="form-label">Monto *</label>
          <input type="number" step="0.01" min="0.01" className="form-control"
            value={form.monto} onChange={(e) => setForm({ ...form, monto: e.target.value })} required />
        </div>
        <button type="submit" className="btn btn-primary w-100" disabled={saving}>
          {saving ? 'Registrando...' : 'Registrar pago mensual'}
        </button>
      </form>
    </div>
  )
}
