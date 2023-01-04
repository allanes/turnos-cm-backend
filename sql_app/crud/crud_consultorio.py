from typing import List
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Consultorio, Medico, Paciente, RegistroConsultorios, Turno
from sql_app.schemas.consultorio import ConsultorioCreate, ConsultorioUpdate, ConsultorioDetallado

class CRUDConsultorio(CRUDBase[Consultorio, ConsultorioCreate, ConsultorioUpdate]):
    def get_consultorios_detallados(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Consultorio]:
        today = datetime.utcnow().date()
        
        consultorios_activos = (
            db.query(RegistroConsultorios)
            .filter(func.date(RegistroConsultorios.fecha) == today)
            .order_by(RegistroConsultorios.fecha.desc())
            .distinct()
            .offset(skip).limit(limit).all()
        )
        print(f'Consuls activos: {len(consultorios_activos)}')
        
        consuls_salida = []
        for consultorio in consultorios_activos:
            db_medico = (db.query(Medico).where(Medico.id==consultorio.id_medico).first())
            
            nombre_medico = f'{db_medico.apellido} {db_medico.nombre}' if db_medico else None
            
            db_turnos = (
                db.query(Turno)
                .filter(func.date(Turno.fecha) == today)
                .filter(Turno.id_medico==db_medico.id)
                .order_by(Turno.fecha.asc())
                .all()
            )
            ids_pacientes = [db_turno.id_paciente for db_turno in db_turnos]
            
            nombres_pacientes = []
            for id_pac in ids_pacientes:
                db_paciente = (db.query(Paciente).where(Paciente.id==id_pac)).first()
                nombre_paciente = f'{db_paciente.apellido} {db_paciente.nombre}' if db_paciente else None
                nombres_pacientes.append(nombre_paciente)
            
            consul = super().get(db=db, id=consultorio.id_consultorio)
            
            consuls_salida.append(
                ConsultorioDetallado(
                    **consul.__dict__, 
                    medico=nombre_medico,
                    pacientes=nombres_pacientes
                )
            )
            
        return consuls_salida
        

consultorio = CRUDConsultorio(Consultorio)