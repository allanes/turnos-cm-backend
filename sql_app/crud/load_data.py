from sqlalchemy.orm import Session
from sql_app.crud import metadata


def init_db(db: Session) -> None:
    for conjunto_ejemplos, modelo_base in zip(metadata.ejemplos, metadata.modelos_base):
        for ejemplo in conjunto_ejemplos:
            db_ejemplo = modelo_base(**ejemplo)
            db.add(db_ejemplo)
        db.commit()
        
def cargar_turnos_ejemplo(db: Session) -> None:
    for conjunto_ejemplos, modelo_base in zip(metadata.ejemplos[-2:], metadata.modelos_base[-2:]):
        for ejemplo in conjunto_ejemplos:
            db_ejemplo = modelo_base(**ejemplo)
            db.add(db_ejemplo)
        db.commit()
        