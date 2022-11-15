from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.security import check_for_user_permission
from sqlalchemy.orm import Session
from app.database.db_init import get_db
from .schemas import *
from . import work_with_smeta
from fastapi.responses import FileResponse
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SMETAS_DIR = os.path.join(BASE_DIR, "smetas")


def make_file_path(user_id: int):
    return os.path.join(SMETAS_DIR, str(user_id) + ".xlsx")


def make_result_path(user_id: int):
    return os.path.join(SMETAS_DIR, str(user_id) + "_result.xlsx")


router = APIRouter(
    prefix="/smeta",
    tags=["smeta"],
    dependencies=[Depends(check_for_user_permission)],
)


@router.post("/parse_smeta/{user_id}", response_model=Smeta)
async def parse_smeta(user_id: int, general_data: ParseSmetaIn, db: Session = Depends(get_db)):
    result = await work_with_smeta.parse_smeta(db, make_file_path(user_id), make_result_path(user_id), general_data)
    return result


@router.post("/save_smeta/{user_id}")
async def save_smeta(user_id: int, file: bytes = File()):
    shutil.copyfile('app/routers/smeta/base.xlsx', make_result_path(user_id))

    path = make_file_path(user_id)
    print(path)
    with open(path, "wb") as save_file:
        save_file.write(file)


patch_mock = False


# TODO хранить имя файла и возвращать с нормальным именем
@router.post("/patch_smeta/{user_id}", response_class=FileResponse)
async def patch_smeta(user_id: int, patches: PatchSmetaIn, db: Session = Depends(get_db)):
    filename = str(user_id) + "_result.xlsx"
    path = make_result_path(user_id)
    await work_with_smeta.patch_smeta(db, path, patches)
    headers = {f'Content-Disposition': f'attachment; filename="{filename}"',
               'Access-Control-Expose-Headers': 'Content-Disposition'}
    return FileResponse(path=path, filename=filename, headers=headers)


@router.get("/")
async def smeta_hello():
    return "Hello from /smeta/"
