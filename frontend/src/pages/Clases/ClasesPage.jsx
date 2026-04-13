import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getClases, createClase } from '../../api/clases'
import AlertMessage from '../../components/AlertMessage'
import LoadingSpinner from '../../components/LoadingSpinner'

function formatDate(isoDate) {
  if (!isoDate) return ''
  const [y, m, d] = isoDate.split('-')
  return `${d}/${m}/${y}`
}

export default function ClasesPage() {
  const navigate = useNavigate()
  const [clases, setClases] = useState([])
  const [loading, setLoading] = useState(true)
  const [alert, setAlert] = useState({ type: 'success', msg: '' })
  const [showForm, setShowForm] = useState(false)
  const [newFecha, setNewFecha] = useState('')
  const [saving, setSaving] = useState(false)
  const [filtro, setFiltro] = useState({ desde: '', hasta: '' })

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const params = {}
      if (filtro.desde) params.desde = filtro.desde
      if (filtro.hasta) params.hasta = filtro.hasta
      setClases(await getClases(params))
    } catch {
      setAlert({ type: 'danger', msg: 'Error al cargar clases' })
    } finally {
      setLoading(false)
    }
  }, [filtro])

  useEffect(() => { load() }, [load])

  async function handleCreate(e) {
    e.preventDefault()
    if (!newFecha) return
    setSaving(true)
    try {
      await createClase({ fecha: newFecha })
      setShowForm(false)
      setNewFecha('')
      setAlert({ type: 'success', msg: 'Clase creada correctamente' })
      load()
    } catch (err) {
      const msg = err.response?.data?.detail || 'Error al crear clase'
      setAlert({ type: 'danger', msg })
    } finally {
      setSaving(false)
    }
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="mb-0">Clases</h4>
        <button className="btn btn-primary" onClick={() => setShowForm(true)}>+ Nueva clase</button>
      </div>

      <AlertMessage type={alert.type} message={alert.msg} onClose={() => setAlert({ ...alert, msg: '' })} />

      <div className="row g-2 mb-3">
        <div className="col-auto">
          <input type="date" className="form-control" placeholder="Desde" value={filtro.desde}
            onChange={(e) => setFiltro({ ...filtro, desde: e.target.value })} />
        </div>
        <div className="col-auto">
          <input type="date" className="form-control" placeholder="Hasta" value={filtro.hasta}
            onChange={(e) => setFiltro({ ...filtro, hasta: e.target.value })} />
        </div>
        <div className="col-auto">
          <button className="btn btn-outline-secondary" onClick={() => setFiltro({ desde: '', hasta: '' })}>
            Limpiar filtro
          </button>
        </div>
      </div>

      {showForm && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Nueva Clase</h5>
                <button className="btn-close" onClick={() => setShowForm(false)} />
              </div>
              <form onSubmit={handleCreate}>
                <div className="modal-body">
                  <label className="form-label">Fecha *</label>
                  <input type="date" className="form-control" value={newFecha}
                    onChange={(e) => setNewFecha(e.target.value)} required />
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowForm(false)}>Cancelar</button>
                  <button type="submit" className="btn btn-primary" disabled={saving}>
                    {saving ? 'Creando...' : 'Crear'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {loading ? <LoadingSpinner /> : (
        <div className="table-responsive">
          <table className="table table-hover">
            <thead className="table-dark">
              <tr>
                <th>Fecha</th>
                <th>Estado</th>
                <th>Asistentes</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {clases.length === 0 && (
                <tr><td colSpan={4} className="text-center text-muted">No hay clases</td></tr>
              )}
              {clases.map((c) => (
                <tr key={c.id}>
                  <td>{formatDate(c.fecha)}</td>
                  <td>
                    <span className={`badge ${c.estado === 'activa' ? 'bg-success' : 'bg-secondary'}`}>
                      {c.estado}
                    </span>
                  </td>
                  <td>{c.total_asistentes}</td>
                  <td>
                    <button
                      className="btn btn-sm btn-outline-primary"
                      onClick={() => navigate(`/clases/${c.id}/asistencia`)}
                    >
                      Ver asistencia
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
