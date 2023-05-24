import os
import subprocess
from typing import Any
from fastapi import Depends, FastAPI, BackgroundTasks, HTTPException, Request
from sqlalchemy.orm import Session

from sql_app import models

from sql_app.crud.load_data import init_db, cargar_turnos_ejemplo
from sql_app.api_v1.api import api_router
from sql_app.database import engine
from sql_app.deps import get_db
from fastapi.middleware.cors import CORSMiddleware
from sql_app.servidor_socketio import sio
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from socketio import ASGIApp

from fastapi.responses import FileResponse
os.environ['DISPLAY'] = ':0'

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Administración de Turnos - Centro Médico Esperanza',
    swagger_ui_parameters={
        'defaultModelsExpandDepth': 0,
        'docExpansion': 'list',
        'requestSnippetsEnabled': True,
        'tryItOutEnabled': True
    },
)
app.include_router(api_router, prefix="/api/v1")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")

origins = [
    "http://localhost",
    "http://localhost:*",
    "http://localhost:5000",
    "http://localhost:3000",
    "http://192.168.100.0/16"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

some_file_path = "notification3.wav"

@app.get("/notification")
async def main():
    return FileResponse(some_file_path)

@app.get("/inicializar_db/")
def inicializar_db(db: Session = Depends(get_db)):
    init_db(db=db)
    
@app.get("/cargar-turnos-ejemplo/")
def inicializar_db(db: Session = Depends(get_db)):
    cargar_turnos_ejemplo(db=db)


def abrir_vistas_teles():
    process = subprocess.Popen(['/bin/bash', '/home/administrador/Escritorio/app_centro_medico/turnos-cm-backend/scripts/abrir_teles.sh'])

@app.get("/abrir-ventanas-teles")
async def handle_abrir_vistas_teles(request:Request, background_tasks: BackgroundTasks):
    client_host = request.client.host

    if client_host.startswith("192.168."):
        background_tasks.add_task(abrir_vistas_teles)
        return {'message': 'Comando enviado correctamente'}
    else:
        return {'message': 'Acceso no autorizado'}

app = ASGIApp(sio, app)
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000, host="0.0.0.0")