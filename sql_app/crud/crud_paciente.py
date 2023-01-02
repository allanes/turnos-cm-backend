from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Paciente
from sql_app.schemas.paciente import PacienteCreate, PacienteUpdate

class CRUDPaciente(CRUDBase[Paciente, PacienteCreate, PacienteUpdate]):
    def create(self, db: Session, *, obj_in: PacienteCreate) -> Paciente:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Paciente]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )


paciente = CRUDPaciente(Paciente)