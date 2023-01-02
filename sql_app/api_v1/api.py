from fastapi import APIRouter

from sql_app.api_v1.endpoints import consultorios, pacientes

api_router = APIRouter()
api_router.include_router(consultorios.router, prefix="/consultorios", tags=["consultorios"])
api_router.include_router(pacientes.router, prefix="/pacientes", tags=["pacientes"])

