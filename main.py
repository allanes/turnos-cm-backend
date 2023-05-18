import os
import subprocess
from typing import Any
from fastapi import Depends, FastAPI, BackgroundTasks
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.api_v1.endpoints.turnos import create_turno, delete_turno
from sql_app.api_v1.endpoints.medicos import next_turn, previous_turn

from sql_app.crud.load_data import init_db, cargar_turnos_ejemplo
from sql_app.api_v1.api import api_router
from sql_app.database import engine
from sql_app.deps import get_db
from fastapi.middleware.cors import CORSMiddleware
from sql_app.servidor_socketio import sio
from fastapi.routing import Mount
from fastapi.responses import FileResponse
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

origins = [
    "http://localhost",
    "http://localhost:*",
    "http://localhost:5000",
    "http://localhost:3000",
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

@app.post("/api/v1/turns/", response_model=schemas.turno.Turno, tags=["Turnos"])
async def handle_create_turno(
    *,
    db: Session = Depends(get_db),
    turno_in: schemas.turno.TurnoCreate,
) -> Any:
    print('Creando turno')
    turno_creado = await create_turno(db=db, turno_in=turno_in)
    
    
    # consultorio = crud.crud_medico.medico.get_ultimo_consultorio_by_medico(db=db, medico_id=turno_creado.id_medico)
    # nro_consul = consultorio.split(' ')[1]
    # print(f'Emitiendo evento refresh para {consultorio}')
    # await sio.emit('refresh', nro_consul)
    # print('Emitiendo evento refresh')
    # await sio.emit('turn-created', '1')
    # print('Evento refresh emitido')
    
    return turno_creado

@app.get("/api/v1/doctors/{id}/nextPatient", response_model=schemas.turno.Turno, tags=["Medicos"])
async def handle_next_turn(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    
    turno_atendido = await next_turn(db=db, id_medico=id)
    consultorio = crud.crud_medico.medico.get_ultimo_consultorio_by_medico(db=db, medico_id=id)
    nro_consul = consultorio.split(' ')[1]

    db_medico = crud.crud_medico.medico.get_with_turns(db=db, id=id)
    
    if not db_medico.turnos:
        raise HTTPException(status_code=404, detail="El Medico no tiene turnos")    
    
    prox_paciente = db_medico.turnos[0].nombre_paciente
    print(f'Nombre del prox paciente: {prox_paciente}')
    
    print(f'Emitiendo evento refresh para {consultorio}')
    await sio.emit('refresh', f'{nro_consul};{prox_paciente}')
    print('Evento refresh emitido')
    
    return turno_atendido

@app.get("/api/v1/doctors/{id}/previousPatient", response_model=schemas.turno.Turno, tags=["Medicos"])
async def handle_previous_turn(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    
    turno_anterior = await previous_turn(db=db, id=id)

    consultorio = crud.crud_medico.medico.get_ultimo_consultorio_by_medico(db=db, medico_id=id)
    nro_consul = consultorio.split(' ')[1]

    # 
    db_medico = crud.crud_medico.medico.get_with_turns(db=db, id=id)
    
    if not db_medico.turnos:
        raise HTTPException(status_code=404, detail="El Medico no tiene turnos")    
    
    prev_paciente = db_medico.turnos[0].nombre_paciente
    print(f'Nombre del prox paciente: {prev_paciente}')

    print(f'Emitiendo evento refresh para {consultorio}')
    await sio.emit('refresh', f'{nro_consul};{prev_paciente}')
    print('Evento refresh emitido')
    
    return turno_anterior

def abrir_vistas_teles():
    process = subprocess.Popen(['/bin/bash', '/home/administrador/Escritorio/app_centro_medico/turnos-cm-backend/scripts/abrir_teles.sh'])

@app.get("/abrir-ventanas-teles")
async def handle_abrir_vistas_teles(background_tasks: BackgroundTasks):
    background_tasks.add_task(abrir_vistas_teles)    
    return {"message": 'Ventanas abiertas correctamente'}

app = ASGIApp(sio, app)
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000, host="0.0.0.0")