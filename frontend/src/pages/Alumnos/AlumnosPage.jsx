import { useState, useEffect, useCallback } from 'react'
import { getAlumnos, deactivateAlumno } from '../../api/alumnos'
import AlumnoForm from './AlumnoForm'
import AlertMessage from '../../components/AlertMessage'
import LoadingSpinner from '../../components/LoadingSpinner'

export default function AlumnosPage() {
  const [alumnos, setAlumnos] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editAlumno, setEditAlumno] = useState(null)
  const [alert, setAlert] = useState({ type: 'success', msg: '' })

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const data = await getAlumnos({ q: search || undefined })
      setAlumnos(data)
    } catch {
      setAlert({ type: 'danger', msg: 'Error al cargar alumnos' })
    } finally {
      setLoading(false)
    }
  }, [search])

  useEffect(() => { load() }, [load])

  function openNew() { setEditAlumno(null); setShowForm(true) }
  function openEdit(a) { setEditAlumno(a); setShowForm(true) }

  async function handleDeactivate(alumno) {
    if (!confirm(`¿Desactivar a ${alumno.nombre} ${alumno.apellido}?`)) return
    try {
      await deactivateAlumno(alumno.id)
      setAlert({ type: 'success', msg: 'Alumno desactivado correctamente' })
      load()
    } catch (err) {
      setAlert({ type: 'danger', msg: err.response?.data?.detail || 'Error al desactivar' })
    }
  }

  function handleSaved() {
    setShowForm(false)
    setAlert({ type: 'success', msg: 'Alumno guardado correctamente' })
    load()
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="mb-0">Alumnos</h4>
        <button className="btn btn-primary" onClick={openNew}>+ Nuevo alumno</button>
      </div>

      <AlertMessage type={alert.type} message={alert.msg} onClose={() => setAlert({ ...alert, msg: '' })} />

      <div className="mb-3">
        <input
          className="form-control"
          placeholder="Buscar por nombre o apellido..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {loading ? <LoadingSpinner /> : (
        <div className="table-responsive">
          <table className="table table-hover">
            <thead className="table-dark">
              <tr>
                <th>Nombre</th>
                <th>Apellido</th>
                <th>Edad</th>
                <th>Teléfono</th>
                <th>Dirección</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {alumnos.length === 0 && (
                <tr><td colSpan={6} className="text-center text-muted">No hay alumnos</td></tr>
              )}
              {alumnos.map((a) => (
                <tr key={a.id}>
                  <td>{a.nombre}</td>
                  <td>{a.apellido}</td>
                  <td>{a.edad}</td>
                  <td>{a.telefono}</td>
                  <td>{a.direccion || '—'}</td>
                  <td>
                    <button className="btn btn-sm btn-outline-primary me-1" onClick={() => openEdit(a)}>Editar</button>
                    <button className="btn btn-sm btn-outline-danger" onClick={() => handleDeactivate(a)}>Desactivar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showForm && (
        <AlumnoForm
          alumno={editAlumno}
          onSaved={handleSaved}
          onCancel={() => setShowForm(false)}
        />
      )}
    </div>
  )
}
