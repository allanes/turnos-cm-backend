from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas

from sql_app.crud.load_data import init_db, cargar_turnos_ejemplo
from sql_app.api_v1.api import api_router
from sql_app.database import engine
from sql_app.deps import get_db
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Administración de Turnos - Centro Médico Esperanza',
    swagger_ui_parameters={
        'defaultModelsExpandDepth': 0,
        'docExpansion': 'list',
        'requestSnippetsEnabled': True,
        'tryItOutEnabled': True
    }
)
app.include_router(api_router, prefix="/api/v1")

origins = {
    "http://localhost",
    "http://localhost:5000",
    "http://localhost:3000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    # allow_headers=["*"],
)

@app.get("/inicializar_db/")
def inicializar_db(db: Session = Depends(get_db)):
    init_db(db=db)
    
@app.get("/cargar-turnos-ejemplo/")
def inicializar_db(db: Session = Depends(get_db)):
    cargar_turnos_ejemplo(db=db)
    

