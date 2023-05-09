from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sql_app.schemas import consultorio
from sql_app.crud import crud_consultorio
from sql_app import crud, models, schemas
from sql_app import deps

router = APIRouter()



@router.get("/", response_model=List[consultorio.Consultorio])
def read_consultorios(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve consultorios.
    """
    consultorios = crud_consultorio.consultorio.get_multi(db, skip=skip, limit=limit)
    return consultorios


@router.post("/", response_model=consultorio.Consultorio)
def create_consultorio(
    *,
    db: Session = Depends(deps.get_db),
    consultorio_in: consultorio.ConsultorioCreate,
) -> Any:
    """
    Create new consultorio.
    """
    consultorios_db = crud_consultorio.consultorio.get_consultorios_por_sala(db=db, sala=consultorio_in.sala)
    print(f'lista de consuls: {consultorios_db}')
    if len(consultorios_db) > 0 and consultorios_db[0].numero == consultorio_in.numero:
        raise HTTPException(status_code=409, detail=f'Office {consultorio_in.numero} in room {consultorio_in.sala} already exists')
    consultorio = crud_consultorio.consultorio.create(db=db, obj_in=consultorio_in)
    return consultorio


@router.put("/{id}", response_model=consultorio.Consultorio)
def update_consultorio(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    consultorio_in: consultorio.ConsultorioUpdate,
) -> Any:
    """
    Update an consultorio.
    """
    consultorio = crud_consultorio.consultorio.get(db=db, id=id)
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultorio not found")
    consultorio = crud_consultorio.consultorio.update(db=db, db_obj=consultorio, obj_in=consultorio_in)
    return consultorio


@router.get("/{id}", response_model=consultorio.Consultorio)
def read_consultorio(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get consultorio by ID.
    """
    consultorio = crud_consultorio.consultorio.get(db=db, id=id)
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultorio not found")
    return consultorio


@router.delete("/{id}", response_model=consultorio.Consultorio)
def delete_consultorio(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an consultorio.
    """
    consultorio = crud_consultorio.consultorio.get(db=db, id=id)
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultorio not found")
    consultorio = crud_consultorio.consultorio.remove(db=db, id=id)
    return consultorio
