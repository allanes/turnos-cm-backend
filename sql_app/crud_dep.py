from sqlalchemy.orm import Session
import metadata
from . import models, schemas_dep


def init_db(db: Session) -> None:
    for conjunto_ejemplos, modelo_base in zip(metadata.ejemplos, metadata.modelos_base):
        for ejemplo in conjunto_ejemplos:
            db_ejemplo = modelo_base(**ejemplo)
            db.add(db_ejemplo)
        db.commit()
        