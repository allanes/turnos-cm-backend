from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas_dep
from sql_app.api_v1.api import api_router
from sql_app.database import engine
from sql_app.deps import get_db
from metadata import fastapi_metadata

models.Base.metadata.create_all(bind=engine)

app = FastAPI(**fastapi_metadata)
app.include_router(api_router, prefix="/api/v1")

@app.get("/inicializar_db/")
def inicializar_db(db: Session = Depends(get_db)):
    crud.init_db(db=db)
    

# **** TURNOS *****
@app.post("/turnos/", response_model=schemas_dep.Turno, tags=['Turnos'])
def post_turno(turno: schemas_dep.TurnoCreate, db: Session = Depends(get_db)):
    db_turno = crud.create_turno(db=db, turno=turno)
    if db_turno is None:
        raise HTTPException(status_code=400, detail="El id de paciente o del médico no existen")
    return db_turno


@app.get("/turnos/", response_model=list[schemas_dep.Turno], tags=['Turnos'])
def list_turnos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    turnos = crud.get_turnos(db, skip=skip, limit=limit)
    return turnos


@app.get("/turnos/{turno_id}", response_model=schemas_dep.Turno, tags=['Turnos'])
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




