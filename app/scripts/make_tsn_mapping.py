from sqlalchemy import create_engine
from app.database import db_models  # noqa - for db initialization
from app.database import schemas as db_schemas
from heapq import heappush, heappop
from collections import defaultdict
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


def count_precision(tp, fp):
    precision = tp / (tp + fp)
    return precision


def count_recall(tp, fn):
    recall = tp / (tp + fn)
    return recall


def count_f_score_between_tsn_and_spgz(tsn_info, spgz_info):
    tp = len(tsn_info.intersection(spgz_info))
    fp = len(tsn_info.difference(spgz_info))
    fn = len(spgz_info.difference(tsn_info))

    precision = count_precision(tp, fp)
    recall = count_recall(tp, fn)
    if precision + recall != 0:
        f_score = 1.09 * precision * recall / (0.3 * precision + recall)
    else:
        f_score = 0
    return precision


def jaccard_metric_between_tsn_and_spgz(tsn_info, spgz_info):
    return len(tsn_info.intersection(spgz_info)) / len(tsn_info.union(spgz_info))


# python -m app.scripts.make_tsn_mapping


async def make_tsn_mapping():
    print("make_hypothesises started to work")
    with SessionLocal() as db:
        all_spgz = (await db_api.sprav_edit.get_all_spgz(db))
        all_hypo = []
        for k, new_tsn in enumerate(await db_api.sprav_edit.get_all_tsn(db)):
            if k % 10 == 0:
                print(k)
            tsn_info = {word for word in new_tsn.tsn_mapping_info.split(',')}
            best_spgzs = []
            for new_spgz in all_spgz:
                spgz_info = {word for word in new_spgz.mapping_info.split(',')}
                score = count_f_score_between_tsn_and_spgz(tsn_info, spgz_info)
                heappush(best_spgzs, (score, new_spgz.id))
                if len(best_spgzs) > 5:
                    heappop(best_spgzs)

            for i in range(5):
                spgz_prob, spgz_id = heappop(best_spgzs)
                tsn_hypothesis = db_schemas.TsnHypothesisCreate(priority=i,
                                                                spgz_piece_id=spgz_id,
                                                                probability=spgz_prob * 100,
                                                                usage_counter=0,
                                                                tsn_piece_id=new_tsn.id)
                all_hypo.append(tsn_hypothesis)

            if k != 0 and k % 1000 == 0:
                tsn_result = await db_api.sprav_edit.add_tsn_hypothesis_bulk(db, all_hypo)
                all_hypo = []



loop = asyncio.get_event_loop()
loop.run_until_complete(make_tsn_mapping())
loop.close()
