from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Turno
from sql_app.schemas.turno import TurnoCreate, TurnoUpdate

class CRUDTurno(CRUDBase[Turno, TurnoCreate, TurnoUpdate]):
    pass

turno = CRUDTurno(Turno)