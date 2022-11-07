from sqlalchemy.orm import Session
from .. import db_models, schemas


async def get_user_by_email(db: Session, email: str):
    return db.query(db_models.User).filter(db_models.User.email == email).first()


async def get_users(db: Session, offset: int = 0, limit: int = 100):
    return db.query(db_models.User).offset(offset).limit(limit).all()


async def get_user_by_id(db: Session, id):
    return db.query(db_models.User).filter(db_models.User.id == id).first()


async def edit_user(db: Session, id: int, level: int):  # двойная запись?
    if await get_user_by_id(db, id) is None:
        return None
    user_edit = schemas.UserEdit(id=id, level=level)
    db.query(db_models.User).filter(db_models.User.id == id).update(user_edit.dict())
    db.commit()
    #db.refresh(user_edit)
    return "Ok" #user_edit



    new_user = db_models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def create_user(db: Session, user: schemas.UserCreate):  # двойная запись?
    new_user = db_models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
