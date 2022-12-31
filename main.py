from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from metadata import fastapi_metadata

models.Base.metadata.create_all(bind=engine)

app = FastAPI(**fastapi_metadata)

# Dependency
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

@app.get("/inicializar_db/")
def inicializar_db(db: Session = Depends(get_db)):
    crud.init_db(db=db)
    

# **** TURNOS *****
@app.post("/turnos/", response_model=schemas.Turno, tags=['Turnos'])
def post_turno(turno: schemas.TurnoCreate, db: Session = Depends(get_db)):
    db_turno = crud.create_turno(db=db, turno=turno)
    if db_turno is None:
        raise HTTPException(status_code=400, detail="El id de paciente o del médico no existen")
    return db_turno


@app.get("/turnos/", response_model=list[schemas.Turno], tags=['Turnos'])
def list_turnos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    turnos = crud.get_turnos(db, skip=skip, limit=limit)
    return turnos


@app.get("/turnos/{turno_id}", response_model=schemas.Turno, tags=['Turnos'])
def get_turno(turno_id: int, db: Session = Depends(get_db)):
    db_turnos = crud.get_turno(db, turno_id=turno_id)
    if db_turnos is None:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return db_turnos

# @app.put("/turnos/{turno_id}", response_model=schemas.Turno, tags=['Turnos'])
# def update_turno(turno_id: int, turno: schemas.TurnoUpdate, db: Session = Depends(get_db)):
#     db_turno = crud.get_turno(db, turno_id=turno_id)
#     if db_turno is None:
#         raise HTTPException(status_code=404, detail="Turno no encontrado")
#     updated_turno = crud.update_turno(db=db, turno_id=db_turno.id, turno_in=turno)
#     return updated_turno

# @app.delete("/turnos/{turno_id}", response_model=schemas.Turno, tags=['Turnos'])
# def delete_turno(turno_id: int, db: Session = Depends(get_db)):
#     db_turno = crud.get_turno(db, turno_id=turno_id)
#     if db_turno is None:
#         raise HTTPException(status_code=404, detail="Turno no encontrado")
#     crud.delete_turno(db=db, turno_id=db_turno.id)
#     return db_turno


# **** MEDICOS *****

@app.get("/medicos/", response_model=list[schemas.Medico], tags=['Medicos'])
def list_medicos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medicos = crud.get_medicos(db, skip=skip, limit=limit)
    return medicos

@app.get("/medicos/{medico_id}", response_model=schemas.Medico, tags=['Medicos'])
def get_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = crud.get_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Medico no encontrado")
    return db_medico

@app.post("/medicos/", response_model=schemas.Medico, tags=['Medicos'])
def post_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    db_medico = crud.create_medico(db=db, medico=medico)
    if db_medico is None:
        raise HTTPException(status_code=400, detail="No se pudo crear el médico")
    return db_medico

# @app.put("/medicos/{medico_id}", response_model=schemas.Medico, tags=['Medicos'])
# def update_medico(medico_id: int, medico: schemas.MedicoUpdate, db: Session = Depends(get_db)):
#     db_medico = crud.get_medico(db, medico_id=medico_id)
#     if db_medico is None:
#         raise HTTPException(status_code=404, detail="Medico no encontrado")
#     updated_medico = crud.update_medico(db=db, medico_id=db_medico.id, medico_update=medico)
#     return updated_medico

# @app.delete("/medicos/{medico_id}", response_model=schemas.Medico, tags=['Medicos'])
# def delete_medico(medico_id: int, db: Session = Depends(get_db)):
#     db_medico = crud.get_medico(db, medico_id=medico_id)
#     if db_medico is None:
#         raise HTTPException(status_code=404, detail="Medico no encontrado")
#     crud.delete_medico(db=db, medico_id=db_medico.id)
#     return db_medico

# **** PACIENTES *****

@app.get("/pacientes/", response_model=list[schemas.Paciente], tags=['Pacientes'])
def list_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pacientes = crud.get_pacientes(db, skip=skip, limit=limit)
    return pacientes

@app.get("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=['Pacientes'])
def get_paciente(paciente_id: int, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente

@app.post("/pacientes/", response_model=schemas.Paciente, tags=['Pacientes'])
def post_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.create_paciente(db=db, paciente=paciente)
    if db_paciente is None:
        raise HTTPException(status_code=400, detail="No se pudo crear el paciente")
    return db_paciente

@app.put("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=['Pacientes'])
def update_paciente(paciente_id: int, paciente: schemas.PacienteUpdate, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    updated_paciente = crud.update_paciente(db=db, paciente_id=db_paciente.id, paciente_update=paciente)
    return updated_paciente

@app.delete("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=['Pacientes'])
def delete_paciente(paciente_id: int, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    crud.delete_paciente(db=db, paciente_id=db_paciente.id)
    return db_paciente


# **** CONSULTORIOS *****

@app.get("/consultorios/", response_model=list[schemas.Consultorio], tags=['Consultorios'])
def get_consultorios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consultorios = crud.get_consultorios(db, skip=skip, limit=limit)
    return consultorios

@app.get("/consultorios/{id}", response_model=schemas.Consultorio, tags=['Consultorios'])
def get_consultorio(id: int, db: Session = Depends(get_db)):
    consultorio = crud.get_consultorio(db=db, consultorio_id=id)
    if consultorio is None:
        raise HTTPException(status_code=404, detail="Consultorio no encontrado")
    return consultorio

@app.post("/consultorios/", response_model=schemas.Consultorio, tags=['Consultorios'])
def update_consultorio(consultorio: schemas.ConsultorioCreate, db: Session = Depends(get_db)):
    consultorio = crud.create_consultorio(db=db, consultorio=consultorio)
    if consultorio is None:
        raise HTTPException(status_code=400, detail="No se pudo crear el paciente")
    
    return crud.update_consultorio(db=db, consultorio_id=id, consultorio=consultorio)

@app.put("/consultorios/{id}", response_model=schemas.Consultorio, tags=['Consultorios'])
def update_consultorio(id: int, consultorio: schemas.ConsultorioUpdate, db: Session = Depends(get_db)):
    consultorio = crud.get_consultorio(db=db, consultorio_id=id)
    if consultorio is None:
        raise HTTPException(status_code=404, detail="Consultorio no encontrado")
    return crud.update_consultorio(db=db, consultorio_id=id, consultorio=consultorio)

@app.delete("/consultorios/{id}", response_model=schemas.Consultorio, tags=['Consultorios'])
def delete_consultorio(id: int, db: Session = Depends(get_db)):
    consultorio = crud.get_consultorio(db=db, consultorio_id=id)
    if consultorio is None:
        raise HTTPException(status_code=404, detail="Consultorio no encontrado")
    return crud.delete_consultorio(db=db, consultorio_id=id)
