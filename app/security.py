from app.database.schemas import EUserLevel
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from app.database.api.users import get_user_by_email
from sqlalchemy.orm import Session
from app.database.db_init import get_db

prod_mode = True


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/get_token")


async def get_user_role(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not prod_mode:
        return EUserLevel.admin
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(db, username)
    if user is None:
        raise credentials_exception
    return user.level


async def check_for_user_permission(role: EUserLevel = Depends(get_user_role)):
    if not prod_mode:
        return
    if role < EUserLevel.user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need to be at least user"
        )


async def check_for_moderator_permission(role: EUserLevel = Depends(get_user_role)):
    if not prod_mode:
        return
    if role < EUserLevel.moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need to be at least moderator"
        )


async def check_for_admin_permission(role: EUserLevel = Depends(get_user_role)):
    if not prod_mode:
        return
    if role < EUserLevel.moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need to be at least admin"
        )
