from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.security import check_for_moderator_permission
from typing import List
import app.database.api as db_api
import app.database.schemas as db_schemas
from app.database.schemas import TsnPieceEdit  # , TsnPieceCreate
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
async def get_spgz(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    kpgz = await db_api.sprav_edit.get_kpgz(db, offset, limit)
    return kpgz


# EDIT ONE PIECE

@router.post("/tsn/edit_one")
async def edit_tsn_piece(update: TsnPieceEdit, db: Session = Depends(get_db)):
    tsn = await db_api.sprav_edit.edit_tsn_piece(db, update)
    if not tsn:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error")
    return "Ok"

# @router.post("/tsn/create_one")
# async def add_tsn_piece(update_in: TsnPieceCreateIn, db: Session = Depends(get_db)):
#    update = TsnPieceCreate(**update_in.dict())
#    tsn = await db_api.sprav_edit.add_tsn_piece(db, update)
#    if not tsn:
#        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error")
#    return "Ok"


# @router.delete("/tsn/{id}")
# async def add_tsn_piece(id: int, db: Session = Depends(get_db)):
#    res = await db_api.sprav_edit.delete_tsn_piece(db, id)
#    if not res:
#        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error")
#    return "Ok"
