from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Consultorios",
        "description": "Endpoints de operaciones CRUD sobre los ***Consultorios***",
    },
    {
        "name": "Pacientes",
        "description": "Endpoints de operaciones CRUD sobre los ***Consultorios***",
    },
    {
        "name": "Medicos",
        "description": "Endpoints de operaciones CRUD sobre los ***Medicos***",
    }, 
]

app = FastAPI(
    title='Administración de Turnos - Centro Médico Esperanza',
    openapi_tags=tags_metadata,
    swagger_ui_parameters={
        'defaultModelsExpandDepth': 0,
        'docExpansion': 'list',
        'requestSnippetsEnabled': True,
        'tryItOutEnabled': True
    }
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# **** MEDICOS *****

@app.post("/medicos/", response_model=schemas.Medico, tags=['Medicos'])
def post_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    # db_user = crud.get_usuario_por_email(db, email=medico.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_medico(db=db, medico=medico)


@app.get("/medicos/", response_model=list[schemas.Medico], tags=['Medicos'])
def list_medicos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medicos = crud.get_medicos(db, skip=skip, limit=limit)
    return medicos


@app.get("/medicos/{medico_id}", response_model=schemas.Medico, tags=['Medicos'])
def get_medico(medico_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_medico(db, medico_id=medico_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# **** PACIENTES *****

@app.post("/pacientes/", response_model=schemas.Paciente, tags=['Pacientes'])
def post_pacientes(
    paciente: schemas.PacienteCreate, db: Session = Depends(get_db)
):
    return crud.create_paciente(db=db, paciente=paciente)

@app.get("/pacientes/", response_model=list[schemas.Paciente], tags=['Pacientes'])
def get_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pacientes = crud.get_pacientes(db, skip=skip, limit=limit)
    return pacientes

# **** CONSULTORIOS *****

@app.post("/consultorios/", response_model=schemas.Consultorio, tags=['Consultorios'])
def post_consultorios(
    consultorio: schemas.ConsultorioCreate, db: Session = Depends(get_db)
):
    return crud.create_consultorio(db=db, consultorio=consultorio)

@app.get("/consultorios/", response_model=list[schemas.Consultorio], tags=['Consultorios'])
def get_consultorios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consultorios = crud.get_consultorios(db, skip=skip, limit=limit)
    return consultorios

@app.get("/consultorios/{id}", response_model=schemas.Consultorio, tags=['Consultorios'])
def get_consultorio(id: int, db: Session = Depends(get_db)):
    consultorio = crud.get_consultorio(db=db, consultorio_id=id)
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultorio not found")
    return consultorio

@app.put("/consultorios/{id}", response_model=schemas.Consultorio, tags=['Consultorios'])
def update_consultorio(
    id: int, consultorio: schemas.ConsultorioUpdate, db: Session = Depends(get_db)
):
    return crud.update_consultorio(db=db, consultorio_id=id, consultorio=consultorio)

@app.delete("/consultorios/{id}", response_model=schemas.Consultorio, tags=['Consultorios'])
def delete_consultorio(id: int, db: Session = Depends(get_db)):
    return crud.delete_consultorio(db=db, consultorio_id=id)
