from fastapi import FastAPI
import app.database.db_init # noqa
from .routers import *
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from dotenv import load_dotenv
from app.database import db_models # noqa - for db initialization
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://130.193.51.59:8000",
    "http://130.193.51.59",
    "http://130.193.51.59:8080",
    "http://130.193.51.59:3000",
    "http://46.73.151.148:3030",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

app.include_router(auth_router)
app.include_router(smeta_router)
app.include_router(sprav_router)
app.include_router(admin_router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

# if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)
