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


def count_f_score_between_sn_and_spgz(sn_info, spgz_info):
    tp = len(sn_info.intersection(spgz_info))
    fp = len(sn_info.difference(spgz_info))
    fn = len(spgz_info.difference(sn_info))

    precision = count_precision(tp, fp)
    recall = count_recall(tp, fn)
    if precision + recall != 0:
        f_score = 1.09 * precision * recall / (0.3 * precision + recall)
    else:
        f_score = 0
    return precision


def jaccard_metric_between_tsn_and_spgz(sn_info, spgz_info):
    return len(sn_info.intersection(spgz_info)) / len(sn_info.union(spgz_info))


# python -m app.scripts.make_tsn_mapping


async def make_tsn_mapping():
    print("make_hypothesises started to work")
    with SessionLocal() as db:
        for new_sn in (await db_api.sprav_edit.get_all_sn(db)):
            sn_info = {word for word in new_sn.sn_mapping_info.split(',')}
            best_spgzs = []
            for new_spgz in (await db_api.sprav_edit.get_all_spgz(db)):
                spgz_info = {word for word in new_spgz.mapping_info.split(',')}
                score = count_f_score_between_sn_and_spgz(sn_info, spgz_info)
                heappush(best_spgzs, (score, new_spgz.id))
                if len(best_spgzs) > 5:
                    heappop(best_spgzs)

            for i, (spgz_prob, spgz_id) in enumerate(best_spgzs):
                tsn_hypothesis = db_schemas.SnHypothesisCreate( priority=i,
                                                                spgz_piece_id=spgz_id,
                                                                probability=spgz_prob * 100,
                                                                usage_counter=0,
                                                                sn_piece_id=new_sn.id)
                tsn_result = await db_api.sprav_edit.add_sn_hypothesis(db, tsn_hypothesis)

        # for curr_tsn in (await db_api.sprav_edit.get_all_tsn(db)):
        #     p_queue = []
        #     heappush(p_queue, 1)
        #     metric = 0
        #     tsn_info = set(curr_tsn.tsn_mapping_info.split(','))
        #     print(curr_tsn.text)
        #     best_spgz = {}
        #     for curr_spgz in all_spgz:
        #         spgz_info = set(curr_spgz.mapping_info.split(','))
        #         new_metric = jaccard_metric_between_tsn_and_spgz(tsn_info, spgz_info)
        #         if new_metric > metric:
        #             metric = new_metric
        #             best_spgz = curr_spgz.name
        #     print(best_spgz)
        #     print(metric)


loop = asyncio.get_event_loop()
loop.run_until_complete(make_tsn_mapping())
loop.close()
