import { useState, useEffect } from 'react'
import client from '../../api/client'
import AlertMessage from '../../components/AlertMessage'
import LoadingSpinner from '../../components/LoadingSpinner'

function formatDT(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('es-AR')
}

export default function AuditoriaPage() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [alert, setAlert] = useState({ type: 'danger', msg: '' })
  const [filtro, setFiltro] = useState({ entidad: '', desde: '', hasta: '' })

  async function load() {
    setLoading(true)
    try {
      const params = {}
      if (filtro.entidad) params.entidad = filtro.entidad
      if (filtro.desde) params.desde = filtro.desde
      if (filtro.hasta) params.hasta = filtro.hasta
      const { data } = await client.get('/auditoria', { params })
      setLogs(data)
    } catch {
      setAlert({ type: 'danger', msg: 'Error al cargar auditoría' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const ENTIDADES = ['alumnos', 'clases', 'asistencias', 'pagos_clase', 'pagos_mensual', 'usuarios']

  return (
    <div>
      <h4 className="mb-3">Registro de Auditoría</h4>
      <AlertMessage type={alert.type} message={alert.msg} onClose={() => setAlert({ ...alert, msg: '' })} />

      <div className="row g-2 mb-3 align-items-end">
        <div className="col-auto">
          <select className="form-select" value={filtro.entidad}
            onChange={(e) => setFiltro({ ...filtro, entidad: e.target.value })}>
            <option value="">Todas las entidades</option>
            {ENTIDADES.map((e) => <option key={e} value={e}>{e}</option>)}
          </select>
        </div>
        <div className="col-auto">
          <input type="date" className="form-control" value={filtro.desde}
            onChange={(e) => setFiltro({ ...filtro, desde: e.target.value })} placeholder="Desde" />
        </div>
        <div className="col-auto">
          <input type="date" className="form-control" value={filtro.hasta}
            onChange={(e) => setFiltro({ ...filtro, hasta: e.target.value })} placeholder="Hasta" />
        </div>
        <div className="col-auto">
          <button className="btn btn-primary" onClick={load}>Filtrar</button>
        </div>
        <div className="col-auto">
          <button className="btn btn-outline-secondary"
            onClick={() => { setFiltro({ entidad: '', desde: '', hasta: '' }); setTimeout(load, 0) }}>
            Limpiar
          </button>
        </div>
      </div>

      {loading ? <LoadingSpinner /> : (
        <div className="table-responsive">
          <table className="table table-sm table-hover">
            <thead className="table-dark">
              <tr>
                <th>Fecha/Hora</th>
                <th>Usuario</th>
                <th>Acción</th>
                <th>Entidad</th>
                <th>ID</th>
                <th>Detalle</th>
              </tr>
            </thead>
            <tbody>
              {logs.length === 0 && (
                <tr><td colSpan={6} className="text-center text-muted">Sin registros</td></tr>
              )}
              {logs.map((l) => (
                <tr key={l.id}>
                  <td style={{ whiteSpace: 'nowrap' }}>{formatDT(l.created_at)}</td>
                  <td>{l.usuario?.username}</td>
                  <td><span className="badge bg-secondary">{l.accion}</span></td>
                  <td>{l.entidad}</td>
                  <td>{l.entidad_id}</td>
                  <td>{l.detalle || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
