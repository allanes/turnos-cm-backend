from typing import List
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Turno
from sql_app.schemas.turno import TurnoCreate, TurnoUpdate

class CRUDTurno(CRUDBase[Turno, TurnoCreate, TurnoUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Turno]:
        today = datetime.now().date()
        db_turnos = db.query(Turno).filter(
            Turno.fecha >= today, 
            Turno.pendiente==True
        ).offset(skip).limit(limit).all()
        
        return db_turnos

turno = CRUDTurno(Turno)