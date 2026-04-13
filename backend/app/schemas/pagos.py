from datetime import date, datetime
from pydantic import BaseModel, field_validator


# ── Pago Clase ──────────────────────────────────────────────

class PagoClaseCreate(BaseModel):
    alumno_id: int
    clase_id: int
    monto: float
    fecha_pago: date

    @field_validator("monto")
    @classmethod
    def monto_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("El monto debe ser mayor que 0")
        return v


class PagoClaseOut(BaseModel):
    id: int
    alumno_id: int
    clase_id: int
    monto: float
    fecha_pago: date
    warning: str | None = None
    created_at: datetime
    anulado: bool

    model_config = {"from_attributes": True}


# ── Pago Mensual ─────────────────────────────────────────────

class PagoMensualCreate(BaseModel):
    alumno_id: int
    mes_cubierto: int
    anio_cubierto: int
    fecha_pago: date
    monto: float

    @field_validator("mes_cubierto")
    @classmethod
    def mes_valid(cls, v: int) -> int:
        if not 1 <= v <= 12:
            raise ValueError("El mes debe estar entre 1 y 12")
        return v

    @field_validator("anio_cubierto")
    @classmethod
    def anio_valid(cls, v: int) -> int:
        if v <= 2000:
            raise ValueError("El año debe ser mayor que 2000")
        return v

    @field_validator("monto")
    @classmethod
    def monto_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("El monto debe ser mayor que 0")
        return v


class PagoMensualOut(BaseModel):
    id: int
    alumno_id: int
    mes_cubierto: int
    anio_cubierto: int
    fecha_pago: date
    monto: float
    created_at: datetime
    anulado: bool

    model_config = {"from_attributes": True}


# ── Anulación ────────────────────────────────────────────────

class AnularRequest(BaseModel):
    motivo: str


class AnularResponse(BaseModel):
    id: int
    anulado: bool
    motivo_anulacion: str | None


# ── Consultas ────────────────────────────────────────────────

class ClaseImpagaItem(BaseModel):
    clase_id: int
    fecha: date


class ClasesImpagasResponse(BaseModel):
    alumno_id: int
    clases_impagas: list[ClaseImpagaItem]


class PagoHistorialItem(BaseModel):
    tipo: str  # "clase" | "mensual"
    id: int
    fecha_pago: date
    monto: float
    anulado: bool
    clase_id: int | None = None
    fecha_clase: date | None = None
    mes_cubierto: int | None = None
    anio_cubierto: int | None = None


class HistorialPagosResponse(BaseModel):
    alumno_id: int
    pagos: list[PagoHistorialItem]


class ReportePagoItem(BaseModel):
    tipo: str
    alumno_id: int
    alumno_nombre: str
    fecha_pago: date
    monto: float
    clase_fecha: date | None = None
    mes_cubierto: int | None = None
    anio_cubierto: int | None = None


class ReportePagosResponse(BaseModel):
    desde: date
    hasta: date
    total_recaudado: float
    pagos: list[ReportePagoItem]
