from datetime import datetime, date
from sqlalchemy import (
    Integer, String, Boolean, Date, DateTime, Numeric, Text,
    ForeignKey, UniqueConstraint, CheckConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    alumnos_creados: Mapped[list["Alumno"]] = relationship(
        "Alumno", foreign_keys="Alumno.created_by", back_populates="creador"
    )
    clases_creadas: Mapped[list["Clase"]] = relationship("Clase", back_populates="creador")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="usuario")


class Alumno(Base):
    __tablename__ = "alumnos"
    __table_args__ = (
        CheckConstraint("edad > 0", name="ck_alumnos_edad"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    direccion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=True)

    creador: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[created_by], back_populates="alumnos_creados")
    asistencias: Mapped[list["Asistencia"]] = relationship("Asistencia", back_populates="alumno")
    pagos_clase: Mapped[list["PagoClase"]] = relationship("PagoClase", back_populates="alumno")
    pagos_mensual: Mapped[list["PagoMensual"]] = relationship("PagoMensual", back_populates="alumno")


class Clase(Base):
    __tablename__ = "clases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False, unique=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="activa")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)

    creador: Mapped["Usuario"] = relationship("Usuario", back_populates="clases_creadas")
    asistencias: Mapped[list["Asistencia"]] = relationship("Asistencia", back_populates="clase")
    pagos_clase: Mapped[list["PagoClase"]] = relationship("PagoClase", back_populates="clase")


class Asistencia(Base):
    __tablename__ = "asistencias"
    __table_args__ = (
        UniqueConstraint("alumno_id", "clase_id", name="uq_asistencia_alumno_clase"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alumno_id: Mapped[int] = mapped_column(Integer, ForeignKey("alumnos.id"), nullable=False)
    clase_id: Mapped[int] = mapped_column(Integer, ForeignKey("clases.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)

    alumno: Mapped["Alumno"] = relationship("Alumno", back_populates="asistencias")
    clase: Mapped["Clase"] = relationship("Clase", back_populates="asistencias")


class PagoClase(Base):
    __tablename__ = "pagos_clase"
    __table_args__ = (
        CheckConstraint("monto > 0", name="ck_pagos_clase_monto"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alumno_id: Mapped[int] = mapped_column(Integer, ForeignKey("alumnos.id"), nullable=False)
    clase_id: Mapped[int] = mapped_column(Integer, ForeignKey("clases.id"), nullable=False)
    monto: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    fecha_pago: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    anulado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    motivo_anulacion: Mapped[str | None] = mapped_column(String(255), nullable=True)

    alumno: Mapped["Alumno"] = relationship("Alumno", back_populates="pagos_clase")
    clase: Mapped["Clase"] = relationship("Clase", back_populates="pagos_clase")


class PagoMensual(Base):
    __tablename__ = "pagos_mensual"
    __table_args__ = (
        CheckConstraint("monto > 0", name="ck_pagos_mensual_monto"),
        CheckConstraint("mes_cubierto BETWEEN 1 AND 12", name="ck_pagos_mensual_mes"),
        CheckConstraint("anio_cubierto > 2000", name="ck_pagos_mensual_anio"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alumno_id: Mapped[int] = mapped_column(Integer, ForeignKey("alumnos.id"), nullable=False)
    mes_cubierto: Mapped[int] = mapped_column(Integer, nullable=False)
    anio_cubierto: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_pago: Mapped[date] = mapped_column(Date, nullable=False)
    monto: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    anulado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    motivo_anulacion: Mapped[str | None] = mapped_column(String(255), nullable=True)

    alumno: Mapped["Alumno"] = relationship("Alumno", back_populates="pagos_mensual")


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    accion: Mapped[str] = mapped_column(String(50), nullable=False)
    entidad: Mapped[str] = mapped_column(String(50), nullable=False)
    entidad_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    detalle: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="audit_logs")
