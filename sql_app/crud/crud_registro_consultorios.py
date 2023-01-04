from datetime import datetime
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import RegistroConsultorios
from sql_app.schemas.registro_consultorios import RegistroConsultoriosCreate, RegistroConsultoriosUpdate

class CRUDRegistroConsultorios(CRUDBase[RegistroConsultorios, RegistroConsultoriosCreate, RegistroConsultoriosUpdate]):        
    pass
    

registro_consultorios = CRUDRegistroConsultorios(RegistroConsultorios)