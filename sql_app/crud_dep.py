from sqlalchemy.orm import Session
import metadata
from . import models, schemas_dep

def standard_creation(db:Session, db_model):
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def get_recepcionistas(db: Session, skip: int = 0, limit: int = 100) -> list[models.Recepcionista]:
    return db.query(models.Recepcionista).offset(skip).limit(limit).all()

def get_recepcionista(db: Session, recepcionista_id: int) -> models.Recepcionista:
    return db.query(models.Recepcionista).filter(models.Recepcionista.id == recepcionista_id).first()

def create_recepcionista(db: Session, recepcionista: schemas_dep.RecepcionistaCreate) -> models.Recepcionista:
    db_recepcionista = models.Recepcionista(**recepcionista.dict())
    return standard_creation(db=db, db_model=db_recepcionista)


def delete_consultorio(db: Session, consultorio_id: int) -> models.Consultorio:
    consultorio = db.query(models.Consultorio).filter(models.Consultorio.id == consultorio_id).first()
    db.delete(consultorio)
    db.commit()
    return consultorio

def get_turno(db: Session, turno_id: int) -> models.Turno:
    return db.query(models.Turno).filter(models.Turno.id == turno_id).first()

def get_turnos(db: Session, skip: int = 0, limit: int = 100) -> list[models.Turno]:
    return db.query(models.Turno).offset(skip).limit(limit).all()

def create_turno(db: Session, turno: schemas_dep.TurnoCreate) -> models.Turno:
    paciente = db.query(models.Paciente).filter(models.Paciente.id == turno.id_paciente).first()
    if not paciente: return None
    medico = db.query(models.Medico).filter(models.Medico.id == turno.id_medico).first()
    if not medico: return None
    
    db_turno = models.Turno(**turno.dict())
    return standard_creation(db=db, db_model=db_turno)


def init_db(db: Session) -> None:
    for conjunto_ejemplos, modelo_base in zip(metadata.ejemplos, metadata.modelos_base):
        for ejemplo in conjunto_ejemplos:
            db_ejemplo = modelo_base(**ejemplo)
            db.add(db_ejemplo)
        db.commit()
        