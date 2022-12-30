from xml.etree.ElementInclude import include
from sqlalchemy.orm import Session

from . import models, schemas


def get_pacientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Paciente).offset(skip).limit(limit).all()

def create_paciente(db: Session, paciente: schemas.PacienteCreate) -> models.Paciente:
    db_paciente = models.Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

def get_medicos(db: Session, skip: int = 0, limit: int = 100) -> list[models.Medico]:
    return db.query(models.Medico).offset(skip).limit(limit).all()

def get_medico(db: Session, medico_id: int) -> models.Medico:
    return db.query(models.Medico).filter(models.Medico.id == medico_id).first()

def create_medico(db: Session, medico: schemas.MedicoCreate) -> models.Medico:
    db_medico = models.Medico(**medico.dict())
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

def get_recepcionistas(db: Session, skip: int = 0, limit: int = 100) -> list[models.Recepcionista]:
    return db.query(models.Recepcionista).offset(skip).limit(limit).all()

def get_recepcionista(db: Session, recepcionista_id: int) -> models.Recepcionista:
    return db.query(models.Recepcionista).filter(models.Recepcionista.id == recepcionista_id).first()

def create_recepcionista(db: Session, recepcionista: schemas.RecepcionistaCreate) -> models.Recepcionista:
    db_recepcionista = models.Recepcionista(**recepcionista.dict())
    db.add(db_recepcionista)
    db.commit()
    db.refresh(db_recepcionista)
    return db_recepcionista

def get_consultorios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Consultorio).offset(skip).limit(limit).all()

def get_consultorio(db: Session, consultorio_id: int) -> models.Consultorio:
    return db.query(models.Consultorio).filter(models.Consultorio.id == consultorio_id).first()

def create_consultorio(db: Session, consultorio: schemas.ConsultorioCreate):
    db_consultorio = models.Consultorio(**consultorio.dict())
    db.add(db_consultorio)
    db.commit()
    db.refresh(db_consultorio)
    return db_consultorio

def update_consultorio(db: Session, consultorio_id:int , consultorio: models.Consultorio) -> models.Consultorio:
    # call get_consultorio by consultorio_id if it exists
    db_consultorio = get_consultorio(db, consultorio_id)
    if not db_consultorio:
        return None
    
    # combine with param consultorio
    update_data = consultorio.dict(exclude_unset=True)

    # update db
    db.query(models.Consultorio).filter(models.Consultorio.id == consultorio_id).update(update_data)
    db.commit()
    db.refresh(db_consultorio)

    # return new synced instance of db_consultorio
    return db_consultorio

def delete_consultorio(db: Session, consultorio_id: int) -> models.Consultorio:
    consultorio = db.query(models.Consultorio).filter(models.Consultorio.id == consultorio_id).first()
    db.delete(consultorio)
    db.commit()
    return consultorio

# def get_usuario(db: Session, user_id: int):
#     return db.query(models.Usuario).filter(models.Usuario.id == user_id).first()


# def get_usuario_por_email(db: Session, email: str):
#     return db.query(models.Usuario).filter(models.Usuario.email == email).first()


# def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Usuario).offset(skip).limit(limit).all()


# def create_usuario(db: Session, user: schemas.UsuarioCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.Usuario(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user