from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Recepcionista
from sql_app.schemas.recepcionista import RecepcionistaCreate, RecepcionistaUpdate

class CRUDRecepcionista(CRUDBase[Recepcionista, RecepcionistaCreate, RecepcionistaUpdate]):
    pass

recepcionista = CRUDRecepcionista(Recepcionista)