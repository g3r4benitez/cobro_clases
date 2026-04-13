from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Asistencia, Clase, PagoClase, PagoMensual
from app.schemas.pagos import PagoClaseCreate, PagoMensualCreate
from app.services.alumnos import get_alumno, assert_alumno_activo


# ── Helpers ──────────────────────────────────────────────────

async def _pago_mensual_activo(db: AsyncSession, alumno_id: int, mes: int, anio: int) -> PagoMensual | None:
    result = await db.execute(
        select(PagoMensual).where(
            PagoMensual.alumno_id == alumno_id,
            PagoMensual.mes_cubierto == mes,
            PagoMensual.anio_cubierto == anio,
            PagoMensual.anulado == False,
        )
    )
    return result.scalar_one_or_none()


# ── Pago Clase ────────────────────────────────────────────────

async def register_pago_clase(
    db: AsyncSession, data: PagoClaseCreate, created_by: int
) -> dict:
    alumno = await get_alumno(db, data.alumno_id)
    assert_alumno_activo(alumno)

    # Check clase exists
    result = await db.execute(select(Clase).where(Clase.id == data.clase_id))
    clase = result.scalar_one_or_none()
    if not clase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clase no encontrada")

    warning = None
    pm = await _pago_mensual_activo(db, data.alumno_id, clase.fecha.month, clase.fecha.year)
    if pm:
        warning = f"El alumno ya tiene pago mensual para {clase.fecha.month}/{clase.fecha.year}"

    pago = PagoClase(
        alumno_id=data.alumno_id,
        clase_id=data.clase_id,
        monto=data.monto,
        fecha_pago=data.fecha_pago,
        created_by=created_by,
    )
    db.add(pago)
    await db.flush()
    await db.refresh(pago)
    return {"pago": pago, "warning": warning}


async def anular_pago_clase(db: AsyncSession, pago_id: int, motivo: str) -> PagoClase:
    result = await db.execute(select(PagoClase).where(PagoClase.id == pago_id))
    pago = result.scalar_one_or_none()
    if not pago:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    pago.anulado = True
    pago.motivo_anulacion = motivo
    await db.flush()
    await db.refresh(pago)
    return pago


# ── Pago Mensual ──────────────────────────────────────────────

async def register_pago_mensual(
    db: AsyncSession, data: PagoMensualCreate, created_by: int
) -> PagoMensual:
    alumno = await get_alumno(db, data.alumno_id)
    assert_alumno_activo(alumno)

    existing = await _pago_mensual_activo(db, data.alumno_id, data.mes_cubierto, data.anio_cubierto)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un pago mensual activo para el alumno en {data.mes_cubierto}/{data.anio_cubierto}",
        )

    pago = PagoMensual(
        alumno_id=data.alumno_id,
        mes_cubierto=data.mes_cubierto,
        anio_cubierto=data.anio_cubierto,
        fecha_pago=data.fecha_pago,
        monto=data.monto,
        created_by=created_by,
    )
    db.add(pago)
    await db.flush()
    await db.refresh(pago)
    return pago


async def anular_pago_mensual(db: AsyncSession, pago_id: int, motivo: str) -> PagoMensual:
    result = await db.execute(select(PagoMensual).where(PagoMensual.id == pago_id))
    pago = result.scalar_one_or_none()
    if not pago:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    pago.anulado = True
    pago.motivo_anulacion = motivo
    await db.flush()
    await db.refresh(pago)
    return pago


# ── Consultas ─────────────────────────────────────────────────

async def get_clases_impagas(db: AsyncSession, alumno_id: int) -> list[dict]:
    # Get all asistencias for this alumno
    result = await db.execute(
        select(Asistencia)
        .options(selectinload(Asistencia.clase))
        .where(Asistencia.alumno_id == alumno_id)
    )
    asistencias = result.scalars().all()

    impagas = []
    for asistencia in asistencias:
        clase = asistencia.clase
        # Check pago por clase
        pc = await db.execute(
            select(PagoClase).where(
                PagoClase.alumno_id == alumno_id,
                PagoClase.clase_id == clase.id,
                PagoClase.anulado == False,
            )
        )
        if pc.scalar_one_or_none():
            continue
        # Check pago mensual
        pm = await _pago_mensual_activo(db, alumno_id, clase.fecha.month, clase.fecha.year)
        if pm:
            continue
        impagas.append({"clase_id": clase.id, "fecha": clase.fecha})

    impagas.sort(key=lambda x: x["fecha"])
    return impagas


async def get_historial_pagos(db: AsyncSession, alumno_id: int) -> list[dict]:
    pagos = []

    pc_result = await db.execute(
        select(PagoClase)
        .options(selectinload(PagoClase.clase))
        .where(PagoClase.alumno_id == alumno_id)
    )
    for p in pc_result.scalars().all():
        pagos.append({
            "tipo": "clase",
            "id": p.id,
            "fecha_pago": p.fecha_pago,
            "monto": float(p.monto),
            "anulado": p.anulado,
            "clase_id": p.clase_id,
            "fecha_clase": p.clase.fecha,
        })

    pm_result = await db.execute(
        select(PagoMensual).where(PagoMensual.alumno_id == alumno_id)
    )
    for p in pm_result.scalars().all():
        pagos.append({
            "tipo": "mensual",
            "id": p.id,
            "fecha_pago": p.fecha_pago,
            "monto": float(p.monto),
            "anulado": p.anulado,
            "mes_cubierto": p.mes_cubierto,
            "anio_cubierto": p.anio_cubierto,
        })

    pagos.sort(key=lambda x: x["fecha_pago"])
    return pagos


async def get_reporte_pagos(db: AsyncSession, desde: date, hasta: date) -> dict:
    pagos = []

    pc_result = await db.execute(
        select(PagoClase)
        .options(selectinload(PagoClase.alumno), selectinload(PagoClase.clase))
        .where(PagoClase.fecha_pago >= desde, PagoClase.fecha_pago <= hasta, PagoClase.anulado == False)
        .order_by(PagoClase.fecha_pago)
    )
    for p in pc_result.scalars().all():
        pagos.append({
            "tipo": "clase",
            "alumno_id": p.alumno_id,
            "alumno_nombre": f"{p.alumno.nombre} {p.alumno.apellido}",
            "fecha_pago": p.fecha_pago,
            "monto": float(p.monto),
            "clase_fecha": p.clase.fecha,
        })

    pm_result = await db.execute(
        select(PagoMensual)
        .options(selectinload(PagoMensual.alumno))
        .where(PagoMensual.fecha_pago >= desde, PagoMensual.fecha_pago <= hasta, PagoMensual.anulado == False)
        .order_by(PagoMensual.fecha_pago)
    )
    for p in pm_result.scalars().all():
        pagos.append({
            "tipo": "mensual",
            "alumno_id": p.alumno_id,
            "alumno_nombre": f"{p.alumno.nombre} {p.alumno.apellido}",
            "fecha_pago": p.fecha_pago,
            "monto": float(p.monto),
            "mes_cubierto": p.mes_cubierto,
            "anio_cubierto": p.anio_cubierto,
        })

    pagos.sort(key=lambda x: x["fecha_pago"])
    total = sum(p["monto"] for p in pagos)
    return {"desde": desde, "hasta": hasta, "total_recaudado": total, "pagos": pagos}
