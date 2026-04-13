import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getClase, registerAsistencia, removeAsistencia } from '../../api/clases'
import { getAlumnos } from '../../api/alumnos'
import AlertMessage from '../../components/AlertMessage'
import LoadingSpinner from '../../components/LoadingSpinner'

function formatDate(isoDate) {
  if (!isoDate) return ''
  const [y, m, d] = isoDate.split('-')
  return `${d}/${m}/${y}`
}

export default function AsistenciaPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [clase, setClase] = useState(null)
  const [loading, setLoading] = useState(true)
  const [alumnos, setAlumnos] = useState([])
  const [selectedIds, setSelectedIds] = useState([])
  const [alert, setAlert] = useState({ type: 'success', msg: '' })
  const [saving, setSaving] = useState(false)

  async function loadClase() {
    try {
      const [c, a] = await Promise.all([getClase(id), getAlumnos()])
      setClase(c)
      setAlumnos(a)
    } catch {
      setAlert({ type: 'danger', msg: 'Error al cargar la clase' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadClase() }, [id])

  const presenteIds = new Set(clase?.asistentes?.map((a) => a.alumno_id) || [])
  const disponibles = alumnos.filter((a) => !presenteIds.has(a.id))

  async function handleAdd() {
    if (!selectedIds.length) return
    setSaving(true)
    try {
      const result = await registerAsistencia(id, selectedIds)
      if (result.ya_presentes?.length > 0) {
        const yaPresentes = result.ya_presentes
          .map((aid) => alumnos.find((a) => a.id === aid))
          .filter(Boolean)
          .map((a) => `${a.apellido}, ${a.nombre}`)
          .join('; ')
        setAlert({ type: 'warning', msg: `Ya presentes: ${yaPresentes}` })
      } else if (result.errores?.length) {
        setAlert({ type: 'warning', msg: result.errores.join(', ') })
      } else {
        setAlert({ type: 'success', msg: 'Asistencia registrada' })
      }
      setSelectedIds([])
      loadClase()
    } catch (err) {
      setAlert({ type: 'danger', msg: err.response?.data?.detail || 'Error al registrar asistencia' })
    } finally {
      setSaving(false)
    }
  }

  async function handleRemove(alumnoId) {
    if (!confirm('¿Quitar asistencia?')) return
    try {
      await removeAsistencia(id, alumnoId)
      setAlert({ type: 'success', msg: 'Asistencia eliminada' })
      loadClase()
    } catch (err) {
      setAlert({ type: 'danger', msg: err.response?.data?.detail || 'Error' })
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div>
      <button className="btn btn-outline-secondary btn-sm mb-3" onClick={() => navigate('/clases')}>
        ← Volver a clases
      </button>
      <h4>Asistencia — {clase ? formatDate(clase.fecha) : ''}</h4>
      {clase && (
        <span className={`badge ${clase.estado === 'activa' ? 'bg-success' : 'bg-secondary'} mb-3`}>
          {clase.estado}
        </span>
      )}

      <AlertMessage type={alert.type} message={alert.msg} onClose={() => setAlert({ ...alert, msg: '' })} />

      <div className="row g-2 mb-3">
        <div className="col">
          <select
            className="form-select"
            multiple
            value={selectedIds}
            onChange={(e) => setSelectedIds(Array.from(e.target.selectedOptions, o => Number(o.value)))}
          >
            <option value="" disabled>Seleccionar alumno(s)...</option>
            {disponibles.map((a) => (
              <option key={a.id} value={a.id}>{a.apellido}, {a.nombre}</option>
            ))}
          </select>
        </div>
        <div className="col-auto">
          <button className="btn btn-primary" onClick={handleAdd} disabled={selectedIds.length === 0 || saving}>
            {saving ? 'Agregando...' : `Agregar${selectedIds.length > 1 ? ` (${selectedIds.length})` : ''}`}
          </button>
        </div>
      </div>

      <h6>Presentes ({clase?.asistentes?.length || 0})</h6>
      <div className="table-responsive">
        <table className="table table-sm">
          <thead>
            <tr><th>Alumno</th><th>Acción</th></tr>
          </thead>
          <tbody>
            {(!clase?.asistentes?.length) && (
              <tr><td colSpan={2} className="text-muted">Sin asistentes registrados</td></tr>
            )}
            {clase?.asistentes?.map((a) => (
              <tr key={a.alumno_id}>
                <td>{a.apellido}, {a.nombre}</td>
                <td>
                  <button
                    className="btn btn-sm btn-outline-danger"
                    onClick={() => handleRemove(a.alumno_id)}
                  >
                    Quitar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
