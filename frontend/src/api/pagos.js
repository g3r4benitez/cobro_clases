import client from './client'

export function registerPagoClase(data) {
  return client.post('/pagos/clase', data).then((r) => r.data)
}

export function anularPagoClase(id, motivo) {
  return client.patch(`/pagos/clase/${id}/anular`, { motivo }).then((r) => r.data)
}

export function registerPagoMensual(data) {
  return client.post('/pagos/mensual', data).then((r) => r.data)
}

export function anularPagoMensual(id, motivo) {
  return client.patch(`/pagos/mensual/${id}/anular`, { motivo }).then((r) => r.data)
}

export function getHistorialPagos(alumnoId) {
  return client.get(`/pagos/alumno/${alumnoId}`).then((r) => r.data)
}

export function getClasesImpagas(alumnoId) {
  return client.get(`/pagos/alumno/${alumnoId}/impagas`).then((r) => r.data)
}

export function getReportePagos(params) {
  return client.get('/pagos/reporte', { params }).then((r) => r.data)
}
