from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Consultorio
from sql_app.schemas.consultorio import ConsultorioCreate, ConsultorioUpdate

class CRUDConsultorio(CRUDBase[Consultorio, ConsultorioCreate, ConsultorioUpdate]):
    pass

consultorio = CRUDConsultorio(Consultorio)