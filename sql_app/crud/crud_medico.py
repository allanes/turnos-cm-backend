from typing import Any
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Medico, Consultorio, RegistroConsultorios
from sql_app.schemas.medico import MedicoCreate, MedicoUpdate

class CRUDMedico(CRUDBase[Medico, MedicoCreate, MedicoUpdate]):
    def exists(self, db: Session, id: Any) -> bool:
        existe = db.query(self.model).filter(self.model.id == id).first()
        return True if existe else False
    
    def get(self, db: Session, id: Any) -> Medico | None:
        db_medico = db.query(self.model).filter(self.model.id == id).first()
        ultimo_consultorio = self.get_ultimo_consultorio_by_medico(db=db, medico_id=db_medico.id)
        medico = db_medico.__dict__
        medico.update({'consultorio': ultimo_consultorio})
        return medico
        
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
            print(f'ultimo consultorio de medico id {db_medico.id}: {ultimo_consultorio}')
            medico = db_medico.__dict__
            medico.update({'consultorio': ultimo_consultorio})
            medicos.append(medico)
            
        return medicos
        
    def remove(self, db: Session, id: int) -> Medico:
        db_obj = db.query(self.model).filter(self.model.id==id)
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
            .order_by(RegistroConsultorios.fecha.desc())
            .first()
        )
        return ultimo_consultorio.descripcion if ultimo_consultorio else None


medico = CRUDMedico(Medico)