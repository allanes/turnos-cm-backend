from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.post("/medicos/", response_model=schemas.Medico)
# def create_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_usuario_por_email(db, email=medico.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_usuario(db=db, user=medico)


# @app.get("/medicos/", response_model=list[schemas.Medico])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_usuarios(db, skip=skip, limit=limit)
#     return users


# @app.get("/medicos/{user_id}", response_model=schemas.Medico)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_usuarios(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@app.post("/pacientes/", response_model=schemas.Paciente)
def create_item_for_user(
    paciente: schemas.PacienteCreate, db: Session = Depends(get_db)
):
    return crud.create_paciente(db=db, paciente=paciente)


@app.get("/pacientes/", response_model=list[schemas.Paciente])
def get_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pacientes = crud.get_pacientes(db, skip=skip, limit=limit)
    return pacientes

@app.post("/consultorios/", response_model=schemas.Consultorio)
def post_consultorio(
    consultorio: schemas.ConsultorioCreate, db: Session = Depends(get_db)
):
    return crud.create_consultorio(db=db, consultorio=consultorio)


@app.get("/consultorios/", response_model=list[schemas.Consultorio])
def get_consultorios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consultorios = crud.get_consultorios(db, skip=skip, limit=limit)
    return consultorios

@app.get("/consultorios/{id}", response_model=schemas.Consultorio)
def get_consultorio(id: int, db: Session = Depends(get_db)):
    consultorio = crud.get_consultorio(db=db, consultorio_id=id)
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultorio not found")
    return consultorio

@app.put("/consultorios/{id}", response_model=schemas.Consultorio)
def update_consultorio(
    id: int, consultorio: schemas.ConsultorioUpdate, db: Session = Depends(get_db)
):
    return crud.update_consultorio(db=db, consultorio_id=id, consultorio=consultorio)

@app.delete("/consultorios/{id}", response_model=schemas.Consultorio)
def delete_consultorio(id: int, db: Session = Depends(get_db)):
    return crud.delete_consultorio(db=db, consultorio_id=id)
