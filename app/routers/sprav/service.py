from fastapi import APIRouter, Depends, HTTPException, status
from app.security import check_for_moderator_permission
from typing import List
import app.database.api as db_api
import app.database.schemas as db_schemas
from app.database.schemas import TsnPieceEdit, SnPieceEdit, SpgzPieceEdit, KpgzPieceEdit
from sqlalchemy.orm import Session
from app.database.db_init import get_db
from app.routers.sprav.schemas import *

router = APIRouter(
    prefix="/sprav",
    tags=["sprav"],
    dependencies=[Depends(check_for_moderator_permission)],
)


@router.get("/")
async def sprav_hello():
    return "Hello from /sprav/"


# GETTERS
## All
@router.get("/tsn", response_model=List[db_schemas.TsnPieceReturn])
async def get_tsn(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tsn = await db_api.sprav_edit.get_tsn(db, offset, limit)
    return tsn


@router.get("/sn", response_model=List[db_schemas.SnPieceReturn])
async def get_sn(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sn = await db_api.sprav_edit.get_sn(db, offset, limit)
    return sn


@router.get("/spgz", response_model=List[db_schemas.SpgzPieceReturn])
async def get_spgz(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    spgz = await db_api.sprav_edit.get_spgz(db, offset, limit)
    return spgz


@router.get("/kpgz", response_model=List[db_schemas.KpgzPieceReturn])
async def get_kpgz(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    kpgz = await db_api.sprav_edit.get_kpgz(db, offset, limit)
    return kpgz


## one

@router.get("/tsn/{id}", response_model=db_schemas.TsnPieceReturn)
async def get_tsn_piece(id: int, db: Session = Depends(get_db)):
    tsn = await db_api.sprav_edit.get_tsn_piece_by_id(db, id)
    return tsn


@router.get("/sn/{id}", response_model=db_schemas.SnPieceReturn)
async def get_sn_piece(id: int, db: Session = Depends(get_db)):
    sn = await db_api.sprav_edit.get_sn_piece_by_id(db, id)
    return sn


@router.get("/spgz/{id}", response_model=db_schemas.SpgzPieceReturn)
async def get_spgz_piece(id: int, db: Session = Depends(get_db)):
    spgz = await db_api.sprav_edit.get_spgz_piece_by_id(db, id)
    return spgz


@router.get("/kpgz/{id}", response_model=db_schemas.KpgzPieceReturn)
async def get_kpgz_piece(id: int, db: Session = Depends(get_db)):
    kpgz = await db_api.sprav_edit.get_kpgz_piece_by_id(db, id)
    return kpgz


# EDIT ONE PIECE

@router.post("/tsn/{id}/edit", response_model=db_schemas.TsnPieceReturn)
async def edit_tsn_piece(id: int, update: TsnPieceEdit, db: Session = Depends(get_db)):
    tsn = await db_api.sprav_edit.edit_tsn_piece(db, update)
    if not tsn:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error")
    return tsn


@router.post("/sn/{id}/edit", response_model=db_schemas.SnPieceReturn)
async def edit_sn_piece(id: int, update: SnPieceEdit, db: Session = Depends(get_db)):
    sn = await db_api.sprav_edit.edit_sn_piece(db, update)
    if not sn:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error")
    return sn


@router.post("/spgz/{user_id}/edit", response_model=db_schemas.SpgzPieceReturn)
async def edit_spgz_piece(user_id: int, update: SpgzPieceEdit, db: Session = Depends(get_db)):
    spgz = await db_api.sprav_edit.edit_spgz_piece(db, update)
    if not spgz:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error")
    return spgz


@router.post("/kpgz/{id}/edit", response_model=db_schemas.KpgzPieceReturn)
async def edit_spgz_piece(id: int, update: KpgzPieceEdit, db: Session = Depends(get_db)):
    kpgz = await db_api.sprav_edit.edit_kpgz_piece(db, update)
    if not kpgz:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error")
    return kpgz


