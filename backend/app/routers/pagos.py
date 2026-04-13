from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.db.models import Usuario
from app.schemas.pagos import (
    PagoClaseCreate, PagoClaseOut, AnularRequest, AnularResponse,
    PagoMensualCreate, PagoMensualOut,
    ClasesImpagasResponse, HistorialPagosResponse, ReportePagosResponse,
)
from app.services.auth import get_current_user
from app.services import pagos as svc
from app.services.auditoria import registrar_accion

router = APIRouter(prefix="/pagos", tags=["pagos"])


# ── Pago Clase ────────────────────────────────────────────────

@router.post("/clase", status_code=201)
async def registrar_pago_clase(
    data: PagoClaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    result = await svc.register_pago_clase(db, data, current_user.id)
    pago = result["pago"]
    warning = result["warning"]
    await registrar_accion(db, current_user.id, "CREATE", "pagos_clase", pago.id)
    return {
        "id": pago.id,
        "alumno_id": pago.alumno_id,
        "clase_id": pago.clase_id,
        "monto": float(pago.monto),
        "fecha_pago": pago.fecha_pago,
        "warning": warning,
        "created_at": pago.created_at,
        "anulado": pago.anulado,
    }


@router.patch("/clase/{pago_id}/anular", response_model=AnularResponse)
async def anular_pago_clase(
    pago_id: int,
    data: AnularRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    pago = await svc.anular_pago_clase(db, pago_id, data.motivo)
    await registrar_accion(db, current_user.id, "UPDATE", "pagos_clase", pago.id, "anulado")
    return {"id": pago.id, "anulado": pago.anulado, "motivo_anulacion": pago.motivo_anulacion}


# ── Pago Mensual ──────────────────────────────────────────────

@router.post("/mensual", response_model=PagoMensualOut, status_code=201)
async def registrar_pago_mensual(
    data: PagoMensualCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    pago = await svc.register_pago_mensual(db, data, current_user.id)
    await registrar_accion(db, current_user.id, "CREATE", "pagos_mensual", pago.id)
    return pago


@router.patch("/mensual/{pago_id}/anular", response_model=AnularResponse)
async def anular_pago_mensual(
    pago_id: int,
    data: AnularRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    pago = await svc.anular_pago_mensual(db, pago_id, data.motivo)
    await registrar_accion(db, current_user.id, "UPDATE", "pagos_mensual", pago.id, "anulado")
    return {"id": pago.id, "anulado": pago.anulado, "motivo_anulacion": pago.motivo_anulacion}


# ── Consultas ─────────────────────────────────────────────────

@router.get("/alumno/{alumno_id}", response_model=HistorialPagosResponse)
async def historial_pagos(
    alumno_id: int,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    pagos = await svc.get_historial_pagos(db, alumno_id)
    return {"alumno_id": alumno_id, "pagos": pagos}


@router.get("/alumno/{alumno_id}/impagas", response_model=ClasesImpagasResponse)
async def clases_impagas(
    alumno_id: int,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    impagas = await svc.get_clases_impagas(db, alumno_id)
    return {"alumno_id": alumno_id, "clases_impagas": impagas}


@router.get("/reporte", response_model=ReportePagosResponse)
async def reporte_pagos(
    desde: date = Query(...),
    hasta: date | None = Query(None),
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    hasta_efectivo = hasta or desde
    return await svc.get_reporte_pagos(db, desde, hasta_efectivo)
