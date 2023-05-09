from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sql_app.schemas import medico, turno
from sql_app.crud import crud_medico, crud_turno, crud_registro_consultorios, crud_consultorio
from sql_app import crud, models, schemas
from sql_app import deps

router = APIRouter()

@router.get("/", response_model=List[medico.Medico])
def read_medicos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve medicos.
    """
    medicos = crud_medico.medico.get_multi_with_consultory(db, skip=skip, limit=limit)
    return medicos

@router.get("/por-sala/{sala}", response_model=List[medico.MedicoConTurnos])
def read_medicos_por_sala(
    sala: str,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve medicos.
    """
    sala = int(sala) if sala.isdigit() else None

    if sala not in [1,2]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La sala debe ser 1 o 2")
    
    lista_registros_consultorios = crud_registro_consultorios.registro_consultorios.get_multi(
        db=db,        
    )

    lista_filtrada = []
    for registro_consul in lista_registros_consultorios:
        consul = crud_consultorio.consultorio.get(db=db, id=registro_consul.id_consultorio)
        if consul.sala == sala:
            lista_filtrada.append(registro_consul)

    lista_registros_consultorios = lista_filtrada.copy()

    medicos = []
    for registro_consul in lista_registros_consultorios:
        medicos.append(
            crud_medico.medico.get_with_turns(db=db, id=registro_consul.id_medico)
        )
    
    return medicos

@router.post("/", response_model=medico.Medico)
def create_medico(
    *,
    db: Session = Depends(deps.get_db),
    medico_in: medico.MedicoCreate,
) -> Any:
    """
    Create new medico.
    """
    db_medico = crud_medico.medico.get(db=db, id=medico_in.id)
    if not db_medico:
        db_medico = crud_medico.medico.create(db=db, obj_in=medico_in)
    else:
        if db_medico.activo:
            raise HTTPException(status_code=409, detail="Medico already exists")
        else:
            print(f'entrando a actualizar el medico')
            db_medico = crud_medico.medico.reactivate(
                db=db, 
                db_obj=db_medico, 
                obj_in=medico_in
            )
        
    return db_medico


@router.put("/{id}", response_model=medico.Medico)
def update_medico(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    medico_in: medico.MedicoUpdate,
) -> Any:
    """
    Update an medico.
    """
    existe = crud_medico.medico.exists(db=db, id=id)
    if not existe:
        raise HTTPException(status_code=404, detail="Medico not found")
    db_medico = crud.medico.get(db=db, id=id)
    db_medico = crud_medico.medico.update(db=db, db_obj=db_medico, obj_in=medico_in)
    return db_medico


@router.get("/{id}", response_model=medico.MedicoConTurnos)
def read_medico(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get medico by ID.
    """
    medico = crud_medico.medico.get_with_turns(db=db, id=id)
    if not medico:
        raise HTTPException(status_code=404, detail="Medico not found")
    return medico


@router.delete("/{id}", response_model=medico.Medico)
def delete_medico(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an medico.
    """
    medico = crud_medico.medico.get(db=db, id=id)
    if not medico:
        raise HTTPException(status_code=404, detail="Medico not found")
    medico = crud_medico.medico.remove(db=db, id=id)
    return medico

# @router.get("/{id}/next", response_model=turno.Turno)
async def next_turn(
    *,
    db: Session, # = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an medico.
    """
    db_medico = crud_medico.medico.get_with_turns(db=db, id=id)
    if not db_medico:
        raise HTTPException(status_code=404, detail="Medico not found")
    if not db_medico.turnos:
        raise HTTPException(status_code=404, detail="El Medico no tiene turnos")
    
    db_turno = crud_turno.turno.get(db=db, id=db_medico.turnos[0].id)
    
    db_turno = crud_turno.turno.update(
        db=db, 
        db_obj=db_turno,
        obj_in={'pendiente': False}
    )

    return db_turno
    
async def previous_turn(
    *,
    db: Session, # = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an medico.
    """
    db_medico = crud_medico.medico.get_with_turns(db=db, id=id)
    
    if not db_medico:
        raise HTTPException(status_code=404, detail="Medico not found")
    
    ultimo_turno = crud_medico.medico.get_ultimo_turno_atendido(db=db, medico_id=id)

    ultimo_turno = crud_turno.turno.update(
        db=db, 
        db_obj=ultimo_turno,
        obj_in={'pendiente': True}
    )
    
    return ultimo_turno