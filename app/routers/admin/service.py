from fastapi import APIRouter, Depends
from app.security import check_for_admin_permission
from sqlalchemy.orm import Session
from app.database.db_init import get_db
import app.database.api as db_api
import app.database.schemas as db_schemas
from typing import List

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(check_for_admin_permission)],
)


@router.get("/")
async def admin_hello():
    return "Hello from /admin/"


@router.get("/users", response_model=List[db_schemas.UserReturn])
async def get_all_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await db_api.users.get_users(db, offset, limit)
    return users

