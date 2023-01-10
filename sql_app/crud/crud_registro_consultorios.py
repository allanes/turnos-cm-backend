from datetime import datetime
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import distinct, exists, func
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import RegistroConsultorios
from sql_app.schemas.registro_consultorios import RegistroConsultoriosCreate, RegistroConsultoriosUpdate

class CRUDRegistroConsultorios(CRUDBase[RegistroConsultorios, RegistroConsultoriosCreate, RegistroConsultoriosUpdate]):        
    def get_multi(self, db: Session) -> List[RegistroConsultorios]:
        today = datetime.now().date()
        subquery = (
            db.query(distinct(RegistroConsultorios.id_medico))
            .filter(RegistroConsultorios.fecha >= today)
            .group_by(RegistroConsultorios.id_consultorio)
            .having(func.max(RegistroConsultorios.id) == RegistroConsultorios.id)
            .subquery()
        )

        db_registro_consultorios = (
            db.query(RegistroConsultorios)
            .filter(RegistroConsultorios.fecha >= today)
            .filter(RegistroConsultorios.id_medico.in_(subquery))
            .group_by(RegistroConsultorios.id_medico)
            .having(func.max(RegistroConsultorios.id) == RegistroConsultorios.id)
            .order_by(RegistroConsultorios.id)
        ).all()
            
        return db_registro_consultorios

registro_consultorios = CRUDRegistroConsultorios(RegistroConsultorios)