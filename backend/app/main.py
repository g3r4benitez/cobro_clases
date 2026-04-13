from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, usuarios, alumnos, clases, pagos, auditoria

app = FastAPI(
    title="KickManager API",
    description="Sistema de gestión de cobro de clases de kickboxing",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PREFIX = "/api/v1"

app.include_router(auth.router, prefix=PREFIX)
app.include_router(usuarios.router, prefix=PREFIX)
app.include_router(alumnos.router, prefix=PREFIX)
app.include_router(clases.router, prefix=PREFIX)
app.include_router(pagos.router, prefix=PREFIX)
app.include_router(auditoria.router, prefix=PREFIX)


@app.get("/health")
async def health():
    return {"status": "ok"}
