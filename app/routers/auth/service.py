from fastapi import APIRouter, Depends, HTTPException, status
from typing import Union
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
import app.database.api as db_api
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .schemas import SignUpIn
import app.database.schemas as db_schemas
import re
from sqlalchemy.orm import Session
from app.database.db_init import get_db
from jose import jwt

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    user = await db_api.users.get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    user_return = db_schemas.UserReturn.from_orm(user)
    return user_return


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/get_token")
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "level": user.level, "email": user.email}


password_pattern = r'[A-Za-z0-9@#$%^&+=]{8,}'


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/sign_up")
async def sign_up(form: SignUpIn, db: Session = Depends(get_db)):
    if not re.fullmatch(password_pattern, form.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    hashed_password = get_password_hash(form.password)
    user_level = db_schemas.check_user_level(form.level)
    user = db_schemas.UserCreate(email=form.email, hashed_password=hashed_password, level=user_level)
    if await db_api.users.get_user_by_email(db, form.email) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="there is already a user with such email")
    result = await db_api.users.create_user(db, user)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return "Ok"
