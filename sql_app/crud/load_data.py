from datetime import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sql_app.models import RegistroConsultorios, Turno
from sql_app.crud import metadata


def init_db(db: Session) -> None:
    for conjunto_ejemplos, modelo_base in zip(metadata.ejemplos[:-2], metadata.modelos_base[:-2]):
        for ejemplo in conjunto_ejemplos:
            db_ejemplo = modelo_base(**ejemplo)
            db.add(db_ejemplo)
        db.commit()
        
def cargar_turnos_ejemplo(db: Session) -> None:
    # for conjunto_ejemplos, modelo_base in zip(metadata.ejemplos[-2:], metadata.modelos_base[-2:]):
    ejemplos_registro_consultorios = metadata.ejemplos[-2]
    for ejemplo in ejemplos_registro_consultorios:
        db_ejemplo = RegistroConsultorios(**ejemplo)
        db.add(db_ejemplo)
    db.commit()

    ejemplos_turnos = metadata.ejemplos[-1]
    for ejemplo in ejemplos_turnos:
        today = datetime.now().date()
        nro_orden = len(db.query(Turno).filter(
            Turno.fecha >= today,
            Turno.id_medico == ejemplo['id_medico']
        ).all())
        nro_orden += 1
        print(f'nro_orden: {nro_orden}')

        # obj_in_data = jsonable_encoder(ejemplo)
        db_ejemplo = Turno(**ejemplo, nro_orden=nro_orden)  # type: ignore
        db.add(db_ejemplo)
        db.commit()
        