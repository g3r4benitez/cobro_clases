import client from './client'

export function getClases(params = {}) {
  return client.get('/clases', { params }).then((r) => r.data)
}

export function createClase(data) {
  return client.post('/clases', data).then((r) => r.data)
}

export function getClase(id) {
  return client.get(`/clases/${id}`).then((r) => r.data)
}

export function cancelClase(id) {
  return client.patch(`/clases/${id}/cancelar`).then((r) => r.data)
}

export function registerAsistencia(claseId, alumnoIds) {
  return client.post(`/clases/${claseId}/asistencia`, { alumno_ids: alumnoIds }).then((r) => r.data)
}

export function removeAsistencia(claseId, alumnoId) {
  return client.delete(`/clases/${claseId}/asistencia/${alumnoId}`).then((r) => r.data)
}
