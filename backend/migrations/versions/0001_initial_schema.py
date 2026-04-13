"""Initial schema — all tables

Revision ID: 0001
Revises:
Create Date: 2026-04-08

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )

    op.create_table(
        "alumnos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("apellido", sa.String(100), nullable=False),
        sa.Column("edad", sa.Integer(), nullable=False),
        sa.Column("telefono", sa.String(20), nullable=False),
        sa.Column("direccion", sa.String(255), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.CheckConstraint("edad > 0", name="ck_alumnos_edad"),
        sa.ForeignKeyConstraint(["created_by"], ["usuarios.id"]),
        sa.ForeignKeyConstraint(["updated_by"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "clases",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("fecha", sa.Date(), nullable=False),
        sa.Column("estado", sa.String(20), nullable=False, server_default="activa"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("fecha"),
    )

    op.create_table(
        "asistencias",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("alumno_id", sa.Integer(), nullable=False),
        sa.Column("clase_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["alumno_id"], ["alumnos.id"]),
        sa.ForeignKeyConstraint(["clase_id"], ["clases.id"]),
        sa.ForeignKeyConstraint(["created_by"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("alumno_id", "clase_id", name="uq_asistencia_alumno_clase"),
    )

    op.create_table(
        "pagos_clase",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("alumno_id", sa.Integer(), nullable=False),
        sa.Column("clase_id", sa.Integer(), nullable=False),
        sa.Column("monto", sa.Numeric(10, 2), nullable=False),
        sa.Column("fecha_pago", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("anulado", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("motivo_anulacion", sa.String(255), nullable=True),
        sa.CheckConstraint("monto > 0", name="ck_pagos_clase_monto"),
        sa.ForeignKeyConstraint(["alumno_id"], ["alumnos.id"]),
        sa.ForeignKeyConstraint(["clase_id"], ["clases.id"]),
        sa.ForeignKeyConstraint(["created_by"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "pagos_mensual",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("alumno_id", sa.Integer(), nullable=False),
        sa.Column("mes_cubierto", sa.Integer(), nullable=False),
        sa.Column("anio_cubierto", sa.Integer(), nullable=False),
        sa.Column("fecha_pago", sa.Date(), nullable=False),
        sa.Column("monto", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("anulado", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("motivo_anulacion", sa.String(255), nullable=True),
        sa.CheckConstraint("monto > 0", name="ck_pagos_mensual_monto"),
        sa.CheckConstraint("mes_cubierto BETWEEN 1 AND 12", name="ck_pagos_mensual_mes"),
        sa.CheckConstraint("anio_cubierto > 2000", name="ck_pagos_mensual_anio"),
        sa.ForeignKeyConstraint(["alumno_id"], ["alumnos.id"]),
        sa.ForeignKeyConstraint(["created_by"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("accion", sa.String(50), nullable=False),
        sa.Column("entidad", sa.String(50), nullable=False),
        sa.Column("entidad_id", sa.Integer(), nullable=True),
        sa.Column("detalle", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("audit_log")
    op.drop_table("pagos_mensual")
    op.drop_table("pagos_clase")
    op.drop_table("asistencias")
    op.drop_table("clases")
    op.drop_table("alumnos")
    op.drop_table("usuarios")
