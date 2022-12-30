from xml.etree.ElementInclude import include
from sqlalchemy.orm import Session

from . import models, schemas


# def create_persona(db: Session, persona: schemas.PersonaCreate, **kwargs):
#     db_persona = models.Persona(**persona.dict())
#     db.add(db_persona)
#     db.commit()
#     db.refresh(db_persona)
#     return db_persona

# def create_persona_desde_paciente(db: Session, paciente: schemas.PacienteCreate):
#     persona = schemas.PersonaCreate(**paciente.dict())
#     return create_persona(db, persona)

# def create_persona_desde_usuario(db: Session, usuario: schemas.UsuarioCreate):
#     persona = schemas.UsuarioCreate(**usuario.dict())
#     return create_persona(db, persona)    

# def get_pacientes(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Paciente).offset(skip).limit(limit).all()

# def create_paciente(db: Session, paciente: schemas.PacienteCreate):
#     db_persona = create_persona_desde_paciente(db, paciente)
#     db_paciente = models.Paciente(id_persona=db_persona.id)
#     db.add(db_paciente)
#     db.commit()
#     db.refresh(db_paciente)
#     return db_paciente

# def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
#     db_persona = create_persona_desde_usuario(db, usuario)
#     db_usuario = models.Usuario(id_persona=db_persona.id)
#     db.add(db_usuario)
#     db.commit()
#     db.refresh(db_usuario)
#     return db_usuario

# def create_recepcionista(db: Session, recepcionista: schemas.RecepcionistaCreate):
#     db_usuario = create_usuario(db, recepcionista)
#     db_recepcionista = models.Recepcionista(id_usuario=db_usuario.id)
#     db.add(db_recepcionista)
#     db.commit()
#     db.refresh(db_recepcionista)
#     return db_recepcionista

def get_consultorios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Consultorio).offset(skip).limit(limit).all()

def get_consultorio(db: Session, consultorio_id: int) -> models.Consultorio:
    return db.query(models.Consultorio).filter(models.Consultorio.id == consultorio_id).first()

def create_consultorio(db: Session, consultorio: schemas.ConsultorioCreate):
    print(f'consultorio dict: {consultorio.dict()}')
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