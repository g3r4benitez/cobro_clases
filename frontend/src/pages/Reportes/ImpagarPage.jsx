import { useState, useEffect } from 'react'
import { getAlumnos } from '../../api/alumnos'
import { getClasesImpagas } from '../../api/pagos'
import AlertMessage from '../../components/AlertMessage'
import LoadingSpinner from '../../components/LoadingSpinner'

function formatDate(d) {
  if (!d) return ''
  const [y, m, day] = d.split('-')
  return `${day}/${m}/${y}`
}

export default function ImpagarPage() {
  const [alumnos, setAlumnos] = useState([])
  const [selectedAlumno, setSelectedAlumno] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(true)
  const [querying, setQuerying] = useState(false)
  const [alert, setAlert] = useState({ type: 'danger', msg: '' })

  useEffect(() => {
    getAlumnos({ incluir_inactivos: true })
      .then(setAlumnos)
      .catch(() => setAlert({ type: 'danger', msg: 'Error al cargar alumnos' }))
      .finally(() => setLoading(false))
  }, [])

  async function handleConsultar() {
    if (!selectedAlumno) return
    setQuerying(true)
    setResult(null)
    try {
      const data = await getClasesImpagas(selectedAlumno)
      setResult(data)
    } catch {
      setAlert({ type: 'danger', msg: 'Error al consultar clases impagas' })
    } finally {
      setQuerying(false)
    }
  }

  const alumnoNombre = alumnos.find((a) => a.id === Number(selectedAlumno))
  const alumnoLabel = alumnoNombre ? `${alumnoNombre.nombre} ${alumnoNombre.apellido}` : ''

  if (loading) return <LoadingSpinner />

  return (
    <div>
      <h4 className="mb-3">Clases Impagas</h4>
      <AlertMessage type={alert.type} message={alert.msg} onClose={() => setAlert({ ...alert, msg: '' })} />

      <div className="row g-2 mb-4 align-items-end">
        <div className="col-md-6">
          <label className="form-label">Alumno</label>
          <select className="form-select" value={selectedAlumno}
            onChange={(e) => { setSelectedAlumno(e.target.value); setResult(null) }}>
            <option value="">Seleccionar alumno...</option>
            {alumnos.map((a) => (
              <option key={a.id} value={a.id}>{a.apellido}, {a.nombre} {!a.activo ? '(inactivo)' : ''}</option>
            ))}
          </select>
        </div>
        <div className="col-auto">
          <button className="btn btn-primary" onClick={handleConsultar}
            disabled={!selectedAlumno || querying}>
            {querying ? 'Consultando...' : 'Consultar'}
          </button>
        </div>
      </div>

      {result && (
        <>
          <p className="text-muted">
            Clases impagas de <strong>{alumnoLabel}</strong>: {result.clases_impagas.length}
          </p>
          {result.clases_impagas.length === 0 ? (
            <div className="alert alert-success">No tiene clases impagas. ✓</div>
          ) : (
            <div className="table-responsive">
              <table className="table table-sm table-bordered">
                <thead className="table-warning">
                  <tr><th>Clase ID</th><th>Fecha</th></tr>
                </thead>
                <tbody>
                  {result.clases_impagas.map((c) => (
                    <tr key={c.clase_id}>
                      <td>{c.clase_id}</td>
                      <td>{formatDate(c.fecha)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  )
}
