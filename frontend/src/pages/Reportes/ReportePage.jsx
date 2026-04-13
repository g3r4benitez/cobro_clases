import { useState } from 'react'
import { getReportePagos } from '../../api/pagos'
import AlertMessage from '../../components/AlertMessage'
import LoadingSpinner from '../../components/LoadingSpinner'

function formatDate(d) {
  if (!d) return ''
  const [y, m, day] = (typeof d === 'string' ? d : d.toISOString().split('T')[0]).split('-')
  return `${day}/${m}/${y}`
}

export default function ReportePage() {
  const [form, setForm] = useState({ desde: '', hasta: '' })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [alert, setAlert] = useState({ type: 'danger', msg: '' })

  async function handleConsultar(e) {
    e.preventDefault()
    if (!form.desde) {
      setAlert({ type: 'warning', msg: 'La fecha "Desde" es requerida' })
      return
    }
    setLoading(true)
    setResult(null)
    try {
      const params = { desde: form.desde }
      if (form.hasta) params.hasta = form.hasta
      setResult(await getReportePagos(params))
    } catch {
      setAlert({ type: 'danger', msg: 'Error al generar reporte' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h4 className="mb-3">Reporte de Pagos</h4>
      <AlertMessage type={alert.type} message={alert.msg} onClose={() => setAlert({ ...alert, msg: '' })} />

      <form onSubmit={handleConsultar} className="row g-2 mb-4 align-items-end">
        <div className="col-auto">
          <label className="form-label">Desde *</label>
          <input type="date" className="form-control" value={form.desde}
            onChange={(e) => setForm({ ...form, desde: e.target.value })} required />
        </div>
        <div className="col-auto">
          <label className="form-label">Hasta</label>
          <input type="date" className="form-control" value={form.hasta}
            onChange={(e) => setForm({ ...form, hasta: e.target.value })} />
        </div>
        <div className="col-auto">
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Generando...' : 'Generar reporte'}
          </button>
        </div>
      </form>

      {loading && <LoadingSpinner />}

      {result && (
        <>
          <div className="d-flex gap-4 mb-3">
            <span className="text-muted">Período: {formatDate(result.desde)} — {formatDate(result.hasta)}</span>
            <span className="fw-bold">Total recaudado: ${result.total_recaudado.toFixed(2)}</span>
          </div>
          {result.pagos.length === 0 ? (
            <div className="alert alert-info">No hay pagos en el período seleccionado.</div>
          ) : (
            <div className="table-responsive">
              <table className="table table-sm table-hover">
                <thead className="table-dark">
                  <tr>
                    <th>Tipo</th>
                    <th>Alumno</th>
                    <th>Fecha pago</th>
                    <th>Detalle</th>
                    <th className="text-end">Monto</th>
                  </tr>
                </thead>
                <tbody>
                  {result.pagos.map((p, i) => (
                    <tr key={i}>
                      <td>
                        <span className={`badge ${p.tipo === 'mensual' ? 'bg-info' : 'bg-primary'}`}>
                          {p.tipo === 'mensual' ? 'Mensual' : 'Clase'}
                        </span>
                      </td>
                      <td>{p.alumno_nombre}</td>
                      <td>{formatDate(p.fecha_pago)}</td>
                      <td>
                        {p.tipo === 'mensual'
                          ? `${p.mes_cubierto}/${p.anio_cubierto}`
                          : p.clase_fecha ? formatDate(p.clase_fecha) : '—'}
                      </td>
                      <td className="text-end">${p.monto.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr className="table-secondary fw-bold">
                    <td colSpan={4} className="text-end">Total:</td>
                    <td className="text-end">${result.total_recaudado.toFixed(2)}</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  )
}
