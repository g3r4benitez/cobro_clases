import client from './client'

export function getAlumnos(params = {}) {
  return client.get('/alumnos', { params }).then((r) => r.data)
}

export function getAlumno(id) {
  return client.get(`/alumnos/${id}`).then((r) => r.data)
}

export function createAlumno(data) {
  return client.post('/alumnos', data).then((r) => r.data)
}

export function updateAlumno(id, data) {
  return client.put(`/alumnos/${id}`, data).then((r) => r.data)
}

export function deactivateAlumno(id) {
  return client.patch(`/alumnos/${id}/desactivar`).then((r) => r.data)
}
