from sqlalchemy import create_engine
from app.database import db_models  # noqa - for db initialization
from app.database import schemas as db_schemas
import app.database.api as db_api
import os
from dotenv import load_dotenv
import psycopg2  # noqa - driver for db
from sqlalchemy.orm import sessionmaker
import asyncio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

engine = create_engine(os.environ["DATABASE_URL"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# TODO bulk insert https://stackoverflow.com/questions/3659142/bulk-insert-with-sqlalchemy-orm

async def make_hypothesises():
    errors = 0
    dealt = 0
    print("make_hypothesises started to work")
    with SessionLocal() as db:
        for id in range(1, await db_api.sprav_edit.count_sn_pieces(db) + 1):
        #for sn_piece_from_db in await db_api.sprav_edit.get_all_sn(db):
            #sn_piece = db_schemas.SnPieceReturn.from_orm(sn_piece_from_db)
            for i in range(1, 6):
                sn_hypothesis = db_schemas.SnHypothesisCreate(priority=i, spgz_piece_id=i, usage_counter=0, sn_piece_id=id)#sn_piece_from_db.id)
                sn_result = await db_api.sprav_edit.add_sn_hypothesis(db, sn_hypothesis)
                if sn_result:
                    dealt += 1
                else:
                    errors += 1
                    print("ERROR")
                    print(sn_hypothesis)
                    print("dealt:", dealt)
        return
        for id in range(1, await db_api.sprav_edit.count_tsn_pieces(db) + 1):
        #for tsn_piece_from_db in await db_api.sprav_edit.get_all_tsn(db):
            #tsn_piece = db_schemas.TsnPieceReturn.from_orm(tsn_piece_from_db)
            for i in range(1, 6):
                tsn_hypothesis = db_schemas.TsnHypothesisCreate(priority=i, spgz_piece_id=i, usage_counter=0, tsn_piece_id=id) #tsn_piece_from_db.id)
                tsn_result = await db_api.sprav_edit.add_tsn_hypothesis(db, tsn_hypothesis)
                if tsn_result:
                    dealt += 1
                else:
                    errors += 1
                    print("ERROR")
                    print(sn_hypothesis)
                    print("dealt:", dealt)
    print("ALL WENT DONE")
    print("dealt:", dealt)

loop = asyncio.get_event_loop()
loop.run_until_complete(make_hypothesises())
loop.close()

