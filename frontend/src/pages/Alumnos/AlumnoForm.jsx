import { useState, useEffect } from 'react'
import { createAlumno, updateAlumno } from '../../api/alumnos'
import AlertMessage from '../../components/AlertMessage'

export default function AlumnoForm({ alumno, onSaved, onCancel }) {
  const [form, setForm] = useState({
    nombre: '',
    apellido: '',
    edad: '',
    telefono: '',
    direccion: '',
  })
  const [errors, setErrors] = useState({})
  const [apiError, setApiError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (alumno) {
      setForm({
        nombre: alumno.nombre || '',
        apellido: alumno.apellido || '',
        edad: alumno.edad || '',
        telefono: alumno.telefono || '',
        direccion: alumno.direccion || '',
      })
    }
  }, [alumno])

  function validate() {
    const e = {}
    if (!form.nombre.trim()) e.nombre = 'El nombre es requerido'
    if (!form.apellido.trim()) e.apellido = 'El apellido es requerido'
    if (!form.edad || Number(form.edad) <= 0) e.edad = 'La edad debe ser mayor que 0'
    if (!form.telefono.trim()) e.telefono = 'El teléfono es requerido'
    return e
  }

  async function handleSubmit(e) {
    e.preventDefault()
    const e2 = validate()
    if (Object.keys(e2).length) { setErrors(e2); return }
    setErrors({})
    setApiError('')
    setLoading(true)
    try {
      const payload = { ...form, edad: Number(form.edad) }
      if (!payload.direccion) delete payload.direccion
      const saved = alumno
        ? await updateAlumno(alumno.id, payload)
        : await createAlumno(payload)
      onSaved(saved)
    } catch (err) {
      const detail = err.response?.data?.detail
      setApiError(typeof detail === 'string' ? detail : 'Error al guardar el alumno')
    } finally {
      setLoading(false)
    }
  }

  function field(label, key, type = 'text', required = true) {
    return (
      <div className="mb-3">
        <label className="form-label">{label}{required && ' *'}</label>
        <input
          type={type}
          className={`form-control ${errors[key] ? 'is-invalid' : ''}`}
          value={form[key]}
          onChange={(e) => setForm({ ...form, [key]: e.target.value })}
        />
        {errors[key] && <div className="invalid-feedback">{errors[key]}</div>}
      </div>
    )
  }

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">{alumno ? 'Editar Alumno' : 'Nuevo Alumno'}</h5>
            <button className="btn-close" onClick={onCancel} />
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body">
              <AlertMessage message={apiError} onClose={() => setApiError('')} />
              {field('Nombre', 'nombre')}
              {field('Apellido', 'apellido')}
              {field('Edad', 'edad', 'number')}
              {field('Teléfono', 'telefono')}
              {field('Dirección', 'direccion', 'text', false)}
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancelar</button>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Guardando...' : 'Guardar'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
