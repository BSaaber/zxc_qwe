from fastapi_sqlalchemy import db


def get_db():
    return db.session
