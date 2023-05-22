from typing import Any
from datetime import datetime

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Medico, Consultorio, RegistroConsultorios, Turno
from sql_app.schemas.medico import MedicoConTurnos, MedicoCreate, MedicoUpdate
from sql_app.schemas.consultorio import Consultorio as ConsultorioSchema

class CRUDMedico(CRUDBase[Medico, MedicoCreate, MedicoUpdate]):
    def exists(self, db: Session, id: Any) -> bool:
        existe = db.query(self.model).filter(self.model.id == id).first()
        return True if existe else False
    
    def __get_consultorios_activos(self, db: Session) -> list[RegistroConsultorios]:
        today = datetime.now().date()

        subquery = (
            db.query(func.max(RegistroConsultorios.id).label("max_id"))
            .group_by(RegistroConsultorios.id_consultorio)
            .subquery()
        )

        consuls_activos = (
            db.query(RegistroConsultorios)
            .filter(RegistroConsultorios.fecha >= today)
            .join(subquery, RegistroConsultorios.id == subquery.c.max_id)
            .filter(RegistroConsultorios.id_medico.isnot(None))
            .order_by(RegistroConsultorios.id_consultorio, RegistroConsultorios.id)
        ).all()

        return consuls_activos
    
    def get_with_turns(self, db: Session, id: Any) -> MedicoConTurnos | None:
        today = datetime.now().date()
        db_medico = db.query(self.model).filter(self.model.id == id, self.model.activo == True).first()
        if not db_medico:
            raise HTTPException(status_code=404, detail="Medico not found")
        
        # Busco los consultorios activos
        consuls_activos = self.__get_consultorios_activos(db=db)

        medicos_atendiendo = [consul_activo.id_medico for consul_activo in consuls_activos]
        print(f'Cantidad de medicos atendiendo: {len(medicos_atendiendo)}')

        turnos = []
        ultimo_consultorio = None
        if id in medicos_atendiendo:
            turnos = db.query(Turno).filter(
                Turno.pendiente==True,
                Turno.fecha >= today,
                Turno.id_medico==db_medico.id
            ).all()
            
            indice = medicos_atendiendo.index(id)
            ultimo_consultorio = consuls_activos[indice].id
            print(f'ultimo consultorio para medico {db_medico.nombre}: {ultimo_consultorio}')
        
        medico_out = MedicoConTurnos(
            **db_medico.__dict__,
            consultorio=ultimo_consultorio,
            turnos=turnos
        )
        return medico_out

    def get_multi_with_consultory(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Medico]:
        db_medicos = (
            db.query(self.model)
            .filter(self.model.activo==True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        medicos = []
        for db_medico in db_medicos:
            ultimo_consultorio = self.get_ultimo_consultorio_by_medico(db=db, medico_id=db_medico.id)
            medico = db_medico.__dict__
            medico.update({'consultorio': ultimo_consultorio})
            medicos.append(medico)
            
        return medicos
        
    def remove(self, db: Session, id: int) -> Medico:
        db_obj = db.query(self.model).filter(self.model.id==id).first()
        setattr(db_obj, 'activo', False)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    def get_ultimo_consultorio_by_medico(self, db: Session, medico_id: int) -> str | None:
        consuls_activos = self.__get_consultorios_activos(db=db)
        medicos_atendiendo = [consul_activo.id_medico for consul_activo in consuls_activos]
        
        ultimo_consultorio = None
        if medico_id in medicos_atendiendo:
            indice = medicos_atendiendo.index(medico_id)
            ultimo_consultorio = consuls_activos[indice]
        
        return f'Consultorio {ultimo_consultorio.id_consultorio}' if ultimo_consultorio else None        
    
    def get_ultimo_turno_atendido(self, db: Session, medico_id: int) -> Turno:
        
        ultimo_turno = (
            db.query(Turno)
            .filter(Turno.pendiente==False)
            .filter(Turno.id_medico == medico_id)
            .order_by(Turno.fecha.desc())
            .first()
        )
        # print(f'tipo de turno: {type(ultimo_turno[0])}')
        return ultimo_turno

    def update(
        self,
        db: Session,
        *,
        db_obj: Medico,
        obj_in: Medico | dict[str, Any]
    ) -> Medico:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def reactivate(self,
        db: Session,
        *,
        db_obj: Medico,
        obj_in: Medico | dict[str, Any]
    ):
        if isinstance(obj_in, dict):
            medico_in_dict = obj_in
        else:
            medico_in_dict = obj_in.dict()
        
        medico_in_dict['activo'] = True
        print(f'datos del medico: {medico_in_dict}')
        return super().update(
            db=db, 
            db_obj=db_obj, 
            obj_in=medico_in_dict
        )
        

medico = CRUDMedico(Medico)