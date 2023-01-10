from typing import Any
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Medico, Consultorio, RegistroConsultorios, Turno
from sql_app.schemas.medico import MedicoConTurnos, MedicoCreate, MedicoUpdate

class CRUDMedico(CRUDBase[Medico, MedicoCreate, MedicoUpdate]):
    def exists(self, db: Session, id: Any) -> bool:
        existe = db.query(self.model).filter(self.model.id == id).first()
        return True if existe else False
    
    def get_with_turns(self, db: Session, id: Any) -> MedicoConTurnos | None:
        today = datetime.now().date()
        db_medico = db.query(self.model).filter(self.model.id == id).first()
        ultimo_consultorio = self.get_ultimo_consultorio_by_medico(db=db, medico_id=db_medico.id)
        turnos = db.query(Turno).filter(
            Turno.pendiente==True,
            Turno.fecha >= today,
            Turno.id_medico==db_medico.id
        ).all()
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
        
    def get_ultimo_consultorio_by_medico(self, db: Session, medico_id: int) -> str:
        today = datetime.now().date()
        # consultorios = db.query(models.Consultorio).join(models.RegistroConsultorios).filter(models.RegistroConsultorios.id_medico == medico_id).order_by(models.RegistroConsultorios.fecha.desc()).limit(5)
        ultimo_consultorio = (
            db.query(Consultorio.descripcion)
            .join(RegistroConsultorios)
            .filter(RegistroConsultorios.fecha >= today)
            .filter(RegistroConsultorios.id_medico == medico_id)
            .order_by(RegistroConsultorios.id.desc())
            .first()
        )
        return ultimo_consultorio.descripcion if ultimo_consultorio else None

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