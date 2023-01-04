from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sql_app.schemas import consultorio
from sql_app import crud, models, schemas_dep
from sql_app import deps

router = APIRouter()


@router.get("/with-details", response_model=List[consultorio.ConsultorioDetallado])
def read_consultorios_con_detalles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve consultorios.
    """
    consultorios = crud.consultorio.get_consultorios_detallados(db, skip=skip, limit=limit)
    return consultorios

@router.get("/", response_model=List[consultorio.Consultorio])
def read_consultorios(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve consultorios.
    """
    consultorios = crud.consultorio.get_multi(db, skip=skip, limit=limit)
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
    consultorio = crud.consultorio.create(db=db, obj_in=consultorio_in)
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
    consultorio = crud.consultorio.get(db=db, id=id)
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultorio not found")
    consultorio = crud.consultorio.update(db=db, db_obj=consultorio, obj_in=consultorio_in)
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
    consultorio = crud.consultorio.get(db=db, id=id)
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
    consultorio = crud.consultorio.get(db=db, id=id)
    if not consultorio:
        raise HTTPException(status_code=404, detail="Consultorio not found")
    consultorio = crud.consultorio.remove(db=db, id=id)
    return consultorio
