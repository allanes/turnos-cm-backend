from typing import List, Any
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Paciente
from sql_app.schemas.paciente import PacienteCreate, PacienteUpdate

class CRUDPaciente(CRUDBase[Paciente, PacienteCreate, PacienteUpdate]):
    def create(self, db: Session, *, obj_in: PacienteCreate) -> Paciente:

        obj_in_data = jsonable_encoder(obj_in)
        
        if obj_in_data['fecha_nacimiento'] and isinstance(obj_in_data['fecha_nacimiento'], str):
            fecha_completa = f'{obj_in_data["fecha_nacimiento"]}T12:00:00.000000'
            obj_in_data['fecha_nacimiento'] = datetime.fromisoformat(fecha_completa)
        
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: Paciente, obj_in: PacienteUpdate | dict[str, Any]
    ) -> Paciente:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        if update_data['fecha_nacimiento'] and isinstance(update_data['fecha_nacimiento'], str):
            fecha_completa = f'{update_data["fecha_nacimiento"]}T12:00:00.000000'
            update_data['fecha_nacimiento'] = datetime.fromisoformat(fecha_completa)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

paciente = CRUDPaciente(Paciente)