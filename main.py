import logging
import os
import subprocess
import signal
import sys
import platform
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
from dotenv import load_dotenv
load_dotenv(os.path.join('ngrok_app', '.env'))
import requests
os.environ['DISPLAY'] = ':0'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
models.Base.metadata.create_all(bind=engine)

# Path to the virtual environment activation script
venv_path_windows = ".venv\\Scripts\\activate.bat"
venv_path_linux = ".venv/Scripts/activate"

# Path to ngrok_server.py
ngrok_server_path = "ngrok_app/server.py"

# Store the ngrok server process
ngrok_server_process = None

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
    "http://192.168.100.0/16",
    "https://6072-2803-9800-a441-82e4-6c61-e48b-44d2-9c0d.ngrok-free.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

some_file_path = "notification3.wav"

@app.on_event("startup")
async def startup_event():
    reverse_proxy_port = os.getenv('NGINX_REVERSE_PROXY_PORT')
    url = f'http://localhost:{reverse_proxy_port}'
    
    try:
        respuesta = requests.get(url=url)
        print(f'Servidor encontrado en {url}. Iniciando ngrok...')
        if respuesta.status_code == 200:
            start_ngrok()
    except requests.exceptions.ConnectionError:
        print(f'No se encontró respuesta en {url}. No se inició ngrok.')

@app.get("/notification")
async def main():
    return FileResponse(some_file_path)

@app.get("/inicializar_db/")
def inicializar_db(db: Session = Depends(get_db)):
    init_db(db=db)
    
@app.get("/cargar-turnos-ejemplo/")
def inicializar_db(db: Session = Depends(get_db)):
    cargar_turnos_ejemplo(db=db)

@app.post("/start_ngrok")
def start_ngrok():
    global ngrok_server_process

    # Check if the ngrok server is already running
    if ngrok_server_process is not None and ngrok_server_process.poll() is None:
        raise HTTPException(status_code=400, detail="ngrok server is already running")

    # Start ngrok_server.py in a new process
    try:
        venv_path = venv_path_linux
        if platform.system == "Windows":
            venv_path = venv_path_windows
        
        ngrok_server_process = subprocess.Popen(
            [sys.executable, ngrok_server_path],
            env={**os.environ, "PATH": f"{venv_path}:{os.environ['PATH']}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "ngrok server started"}

@app.post("/stop_ngrok")
def stop_ngrok():
    global ngrok_server_process

    # Check if the ngrok server is running
    if ngrok_server_process is None or ngrok_server_process.poll() is not None:
        raise HTTPException(status_code=400, detail="ngrok server is not running")

    # Kill the ngrok_server.py process
    try:
        if platform.system() == "Windows":
            ngrok_server_process.terminate()
        else:
            ngrok_server_process.send_signal(signal.SIGTERM)
        ngrok_server_process = None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "ngrok server stopped"}

@app.post('/restart_ngrok')
def handle_restart_ngrok():
    global ngrok_server_process

    # Check if the ngrok server is running
    is_running = True
    if ngrok_server_process is None or ngrok_server_process.poll() is not None:
        # raise HTTPException(status_code=400, detail="ngrok server is not running")
        is_running = False

    # Kill the ngrok_server.py process
    if is_running:
        try:
            if platform.system() == "Windows":
                ngrok_server_process.terminate()
            else:
                ngrok_server_process.send_signal(signal.SIGTERM)
                print("ngrok server stopped")
            ngrok_server_process = None
        except Exception as e:
            # raise HTTPException(status_code=500, detail=str(e))
            print(f'No se pudo detener el tunel de ngrok. Detalle: {str(e)}')

    # Start ngrok_server.py in a new process
    try:
        venv_path = venv_path_linux
        if platform.system == "Windows":
            venv_path = venv_path_windows
        
        ngrok_server_process = subprocess.Popen(
            [sys.executable, ngrok_server_path],
            env={**os.environ, "PATH": f"{venv_path}:{os.environ['PATH']}"}
        )
        mensaje = 'Tunel de ngrok inicializado'
        print(mensaje)
    except Exception as e:
        print(f'No se pudo iniciar el tunel de ngrok. Detalle: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

    return {'message': mensaje}


@app.get("/lista-videos-gdrive")
def read_videos():
    video_urls = [
        "https://drive.google.com/file/d/1Jmh5SLGlgVXmSUKePVhBnOZZBRfjOQi0/view?usp=share_link",  # Rick Astley - Never Gonna Give You Up
        "https://drive.google.com/file/d/1Ljp9p5j3JqIJ09eT9LhRRBlI4spo81jz/view?usp=share_link"
        # "https://www.youtube.com/watch?v=3tmd-ClpJxA",  # a-ha - Take On Me
        # "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",  # Queen - Bohemian Rhapsody
    ]
    return video_urls

@app.get("/carpeta-videos")
def read_videos():
    folder_url = "https://drive.google.com/drive/folders/1Nh5g6dpXgtAyIOsbb-IQanFo8qgJoTIY?usp=sharing"
    return folder_url

@app.get("/lista-videos-locales")
def read_videos():
    video_files = os.listdir('videos')
    video_files = ["http://localhost:8000/videos/"+file for file in video_files]
    return video_files

@app.get("/video/{video_id}")
async def get_video(video_id: str):
    video_directory = os.getcwd() + "/videos/"
    video_files = os.listdir(video_directory)
    if video_id not in video_files:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return FileResponse(video_directory + video_id)

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
    
@app.get("/descargas/descargar_qr", tags=["Downloads"])
async def descargar_qr():
    try:
        file_full_path = os.path.join(BASE_DIR, "descargas", "QR_Medicos.pdf")
        return FileResponse(file_full_path, media_type='application/pdf')
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado ({file_full_path})")

@app.get("/descargas/manual_iniciar_teles", tags=["Downloads"])
async def descargar_manual_iniciar_teles():
    try:
        file_full_path = os.path.join(BASE_DIR, "descargas", "Manual_iniciar_televisores.pdf")
        print(f'Buscando archivo {file_full_path}')
        return FileResponse(file_full_path, media_type='application/pdf')
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado ({file_full_path})")

@app.get("/descargas/manual_apagar_teles", tags=["Downloads"])
async def descargar_manual_apagar_teles():
    try:
        file_full_path = os.path.join(BASE_DIR, "descargas", "Manual_apagar_televisores.pdf")
        print(f'Buscando archivo {file_full_path}')
        return FileResponse(file_full_path, media_type='application/pdf')
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado ({file_full_path})")

app = ASGIApp(sio, app)
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000, host="0.0.0.0")