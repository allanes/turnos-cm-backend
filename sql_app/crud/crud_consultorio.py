from typing import List
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.crud import crud_consultorio, crud_registro_consultorios
from sql_app.models import Consultorio, Medico, Paciente, RegistroConsultorios, Turno
from sql_app.schemas.consultorio import ConsultorioCreate, ConsultorioUpdate, ConsultorioDetallado, Consultorio as ConsultorioSchema

class CRUDConsultorio(CRUDBase[Consultorio, ConsultorioCreate, ConsultorioUpdate]):
    def get_consultorios_por_sala(self, db: Session, sala:int, *, skip: int = 0, limit: int = 100) -> List[Consultorio]:
        db_consultorios = db.query(Consultorio).filter(Consultorio.sala == sala).offset(skip).limit(limit).all()
        
        return db_consultorios
    
    
    def get_consultorios_detallados(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ConsultorioDetallado]:
        today = datetime.now().date()
        
        consultorios_activos = crud_registro_consultorios.registro_consultorios.get_multi(db=db)
        print(f'consultorios activos: {[consultorio.id_consultorio for consultorio in consultorios_activos]}')
        consuls_salida = []
        for consultorio in consultorios_activos:
            db_medico = (db.query(Medico).where(Medico.id==consultorio.id_medico).first())
            nombre_medico = f'{db_medico.apellido} {db_medico.nombre}' if db_medico else None
            
            db_turnos = (
                db.query(Turno)
                .filter(func.date(Turno.fecha) == today)
                .filter(Turno.pendiente == True)
                .filter(Turno.id_medico==db_medico.id)
                .order_by(Turno.fecha.asc())
                .all()
            )
            ids_pacientes = [db_turno.id_paciente for db_turno in db_turnos]
            
            if not ids_pacientes:
                nombres_pacientes = None
            else:
                nombres_pacientes = []
                for id_pac in ids_pacientes:
                    db_paciente = (db.query(Paciente).where(Paciente.id==id_pac)).first()
                    nombre_paciente = f'{db_paciente.apellido} {db_paciente.nombre}' if db_paciente else None
                    nombres_pacientes.append(nombre_paciente)
            
            consul = super().get(db=db, id=consultorio.id_consultorio)
            if consul:
                consul_nuevo = ConsultorioDetallado(
                    **consul.__dict__, 
                    medico=nombre_medico,
                    pacientes=nombres_pacientes
                )
            else:
                consul_nuevo = None
                
            consuls_salida.append(consul_nuevo)
            
        return consuls_salida
    
    def create(self, db: Session, *, obj_in: ConsultorioCreate) -> Consultorio:
        db_consultorios = super().get_multi(db=db)
        cantidad_consuls = len(db_consultorios) if db_consultorios else 0
        obj_in.numero = cantidad_consuls + 1
        return super().create(db, obj_in=obj_in)
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ConsultorioSchema]:
        db_consultorios = super().get_multi(db, skip=skip, limit=limit)
        
        consuls_out = [ConsultorioSchema(
            **db_consultorio.__dict__,
            descripcion=f'Consultorio {db_consultorio.numero}'
        ) for db_consultorio in db_consultorios]
        
        return consuls_out
        

consultorio = CRUDConsultorio(Consultorio)