from fastapi import APIRouter

from sql_app.api_v1.endpoints import (
    consultorios, 
    pacientes, 
    medicos, 
    registros_consultorios, 
    turnos,
    recepcionistas,
    videos
)

api_router = APIRouter()
api_router.include_router(consultorios.router, prefix="/offices", tags=["Consultorios"])
api_router.include_router(pacientes.router, prefix="/patients", tags=["Pacientes"])
api_router.include_router(recepcionistas.router, prefix="/receptionists", tags=["Recepcionistas"])
api_router.include_router(medicos.router, prefix="/doctors", tags=["Medicos"])
api_router.include_router(registros_consultorios.router, prefix="/offices-to-doctors", tags=["Registro de consultorios con médicos"])
api_router.include_router(turnos.router, prefix="/turns", tags=["Turnos"])
api_router.include_router(videos.router, prefix="/video-control", tags=["Videos"])

