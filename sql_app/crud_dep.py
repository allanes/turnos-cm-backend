from sqlalchemy.orm import Session
import metadata
from . import models, schemas_dep

def standard_creation(db:Session, db_model):
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def get_pacientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Paciente).offset(skip).limit(limit).all()

def get_paciente(db: Session, paciente_id: int) -> models.Paciente:
    return db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()

def create_paciente(db: Session, paciente: schemas_dep.PacienteCreate) -> models.Paciente:
    db_paciente = models.Paciente(**paciente.dict())
    return standard_creation(db=db, db_model=db_paciente)

def update_paciente(db: Session, paciente_id: int, paciente: schemas_dep.PacienteUpdate) -> models.Paciente:
    db_paciente = get_paciente(db, paciente_id)
    if not db_paciente:
        return None
    
    update_data = paciente.dict(exclude_unset=True)
    db.query(models.Paciente).filter(models.Paciente.id == paciente_id).update(update_data)
    db.commit()
    db.refresh(db_paciente)

    return db_paciente

def delete_paciente(db: Session, paciente_id: int) -> models.Paciente:
    paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    db.delete(paciente)
    db.commit()
    return paciente

def get_ultimo_consultorio_by_medico(db: Session, medico_id: int) -> str:
    # consultorios = db.query(models.Consultorio).join(models.RegistroConsultorios).filter(models.RegistroConsultorios.id_medico == medico_id).order_by(models.RegistroConsultorios.fecha.desc()).limit(5)
    
    ultimo_consultorio = (
        db.query(models.Consultorio.descripcion)
        .join(models.RegistroConsultorios)
        .filter(models.RegistroConsultorios.id_medico == medico_id)
        .order_by(models.RegistroConsultorios.fecha.desc())
        .first()
    )
    return ultimo_consultorio.descripcion if ultimo_consultorio else None
    

def get_medicos(db: Session, skip: int = 0, limit: int = 100) -> list[models.Medico]:
    db_medico = db.query(models.Medico)\
        .filter(models.Medico.activo==True)\
        .limit(limit)\
        .all()
    return db_medico


def get_medico(db: Session, medico_id: int) -> models.Medico:
    db_medico = db.query(models.Medico).filter(models.Medico.id == medico_id).first()
    
    return db_medico

def create_medico(db: Session, medico: schemas_dep.MedicoCreate) -> models.Medico:
    db_medico = models.Medico(**medico.dict())
    db_medico = standard_creation(db=db, db_model=db_medico)
    consultorios = get_ultimo_consultorio_by_medico(db, medico_id=db_medico.id)
    db_medico.consultorio = consultorios.first()
    return db_medico

def delete_medico(db: Session, medico_id: int) -> models.Medico:
    medico = db.query(models.Medico).filter(models.Medico.id == medico_id).update({'activo': False})
    db.commit()
    db.refresh(medico)
    return medico

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
        