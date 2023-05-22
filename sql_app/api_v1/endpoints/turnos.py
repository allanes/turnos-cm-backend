from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sql_app.schemas import turno
from sql_app.crud import crud_turno
from sql_app import crud, models, schemas
from sql_app import deps
from sql_app.servidor_socketio import sio

router = APIRouter()

@router.get("/", response_model=List[turno.Turno])
def read_turnos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve turnos.
    """
    turnos = crud_turno.turno.get_multi(db, skip=skip, limit=limit)
    return turnos


@router.post("/", response_model=turno.Turno)
async def create_turno(
    *,
    db: Session = Depends(deps.get_db),
    turno_in: turno.TurnoCreate,
) -> Any:
    """
    Create new turno.
    """
    print('Creando nuevo turnardo')
    db_paciente = crud.paciente.get(db=db, id=turno_in.id_paciente)
    
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente not found")
    
    db_medico = crud.medico.get(db=db, id=turno_in.id_medico)
    
    if not db_medico:
        raise HTTPException(status_code=404, detail="Medico not found")
    
    turno = crud_turno.turno.create(db=db, obj_in=turno_in)

    consultorio = crud.crud_medico.medico.get_ultimo_consultorio_by_medico(db=db, medico_id=turno_in.id_medico)
    nro_consul = consultorio.split(' ')[1]

    await sio.emit('created-turn', f'{nro_consul}')

    return turno


@router.put("/{id}", response_model=turno.Turno)
def update_turno(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    turno_in: turno.TurnoUpdate,
) -> Any:
    """
    Update an turno.
    """
    turno = crud_turno.turno.get(db=db, id=id)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno not found")
    turno = crud_turno.turno.update(db=db, db_obj=turno, obj_in=turno_in)
    return turno


@router.get("/{id}", response_model=turno.Turno)
def read_turno(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get turno by ID.
    """
    turno = crud_turno.turno.get(db=db, id=id)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno not found")
    return turno


@router.delete("/{id}", response_model=turno.Turno)
def delete_turno(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an turno.
    """
    turno = crud_turno.turno.get(db=db, id=id)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno not found")
    turno = crud_turno.turno.remove(db=db, id=id)
    return turno
