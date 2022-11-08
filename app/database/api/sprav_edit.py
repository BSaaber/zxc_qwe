from sqlalchemy.orm import Session
from .. import db_models, schemas


# TODO переназвать файл

# returning None if something goes wrong


async def get_tsn_piece_by_code(db: Session, code: str):
    return db.query(db_models.TsnPiece).filter(db_models.TsnPiece.code == code).first()


async def get_sn_piece_by_code(db: Session, code: str):
    return db.query(db_models.SnPiece).filter(db_models.SnPiece.code == code).first()


async def get_tsn(db: Session, offset: int = 0, limit: int = 100):
    return db.query(db_models.TsnPiece).offset(offset).limit(limit).all()


async def count_tsn_pieces(db: Session):
    return db.query(db_models.TsnPiece).count()


async def get_sn(db: Session, offset: int = 0, limit: int = 100):
    return db.query(db_models.SnPiece).offset(offset).limit(limit).all()


async def get_spgz(db: Session, offset: int = 0, limit: int = 100):
    return db.query(db_models.SpgzPiece).offset(offset).limit(limit).all()


async def get_kpgz(db: Session, offset: int = 0, limit: int = 100):
    return db.query(db_models.KpgzPiece).offset(offset).limit(limit).all()


async def count_sn_pieces(db: Session):
    return db.query(db_models.SnPiece).count()


async def get_all_tsn(db: Session):
    return db.query(db_models.TsnPiece).all()


async def get_all_spgz(db: Session):
    return db.query(db_models.SpgzPiece).all()


async def get_all_sn(db: Session):
    return db.query(db_models.SnPiece).all()


async def delete_tsn_piece(db: Session, id: int):
    delete_result = db.query(db_models.TsnPiece).filter(db_models.TsnPiece.id == id).delete()
    if delete_result != 1:
        return None
    return delete_result


async def delete_sn_piece(db: Session, id: int):
    delete_result = db.query(db_models.SnPiece).filter(db_models.SnPiece.id == id).delete()
    if delete_result != 1:
        return None
    return delete_result


async def edit_tsn_piece(db: Session, tsn_piece: schemas.TsnPieceEdit):  # двойная запись?
    update = {k: v for k, v in tsn_piece.dict().items() if v is not None}
    if "spgz_piece_id" in update:
        if await get_spgz_piece_by_id(db, update["spgz_piece_id"]) is None:
            return None
    del update["id"]
    db.query(db_models.TsnPiece).filter(db_models.TsnPiece.id == tsn_piece.id).update(update)
    db.commit()
    db.refresh(tsn_piece)
    return tsn_piece


async def edit_sn_piece(db: Session, sn_piece: schemas.SnPieceEdit):  # двойная запись?
    update = {k: v for k, v in sn_piece.dict().items() if v is not None}
    if "spgz_piece_id" in update:
        if await get_spgz_piece_by_id(db, update["spgz_piece_id"]) is None:
            return None
    del update["id"]
    db.query(db_models.SnPiece).filter(db_models.SnPiece.id == sn_piece.id).update(update)
    db.commit()
    db.refresh(sn_piece)
    return sn_piece


async def add_tsn_piece_without_spgz(db: Session, tsn_piece: schemas.TsnPieceCreateWithoutSpgz):  # двойная запись?
    new_tsn_piece = db_models.TsnPiece(**tsn_piece.dict())
    db.add(new_tsn_piece)
    db.commit()
    db.refresh(new_tsn_piece)
    return new_tsn_piece


async def add_sn_hypothesis(db: Session, hypothesis: schemas.SnHypothesisCreate):
    new_hypothesis = db_models.SnHypothesis(**hypothesis.dict())
    db.add(new_hypothesis)
    db.commit()
    db.refresh(new_hypothesis)
    return new_hypothesis


async def get_tsn_hypothesises_by_tsn_id(db: Session, tsn_piece_id: str):
    return db.query(db_models.TsnHypothesis).filter(db_models.TsnHypothesis.tsn_piece_id == tsn_piece_id).all()


async def get_sn_hypothesises_by_sn_id(db: Session, sn_piece_id: str):
    return db.query(db_models.SnHypothesis).filter(db_models.SnHypothesis.sn_piece_id == sn_piece_id).all()


async def add_tsn_hypothesis(db: Session, hypothesis: schemas.TsnHypothesisCreate):
    new_hypothesis = db_models.TsnHypothesis(**hypothesis.dict())
    db.add(new_hypothesis)
    db.commit()
    db.refresh(new_hypothesis)
    return new_hypothesis


async def add_tsn_hypothesis_bulk(db: Session, hypothesises):
    hypothesises = [db_models.TsnHypothesis(**i.dict()) for i in hypothesises]
    db.bulk_save_objects(hypothesises)


async def add_sn_hypothesis_bulk(db: Session, hypothesises):
    hypothesises = [db_models.SnHypothesis(**i.dict()) for i in hypothesises]
    db.bulk_save_objects(hypothesises)


async def add_sn_piece_without_spgz(db: Session, sn_piece: schemas.SnPieceCreateWithoutSpgz):  # двойная запись?
    new_sn_piece = db_models.SnPiece(**sn_piece.dict())
    db.add(new_sn_piece)
    db.commit()
    db.refresh(new_sn_piece)
    return new_sn_piece


async def add_kpgz_piece(db: Session, kpgz_piece: schemas.KpgzPieceCreate):
    new_kpgz_piece = db_models.KpgzPiece(**kpgz_piece.dict())
    db.add(new_kpgz_piece)
    db.commit()
    db.refresh(new_kpgz_piece)
    return new_kpgz_piece


async def get_spgz_piece_by_id(db: Session, id: int):
    return db.query(db_models.SpgzPiece).filter(db_models.SpgzPiece.id == id).first()


async def get_spgz_piece_by_data_id(db: Session, data_id: int):
    return db.query(db_models.SpgzPiece).filter(db_models.SpgzPiece.data_id == data_id).first()


# async def get_spgz_pieces_by_id_list(db: Session, id_list):
#    return db.query(db_models.SpgzPiece).filter(db_models.SpgzPiece.id.in_(id_list)).all()


async def get_kpgz_piece_by_id(db: Session, id: int):
    return db.query(db_models.KpgzPiece).filter(db_models.KpgzPiece.id == id).first()


async def get_kpgz_piece_by_name(db: Session, name: str):
    return db.query(db_models.KpgzPiece).filter(db_models.KpgzPiece.name == name).first()


async def add_spgz_piece(db: Session, spgz_piece: schemas.SpgzPieceCreate):
    new_spgz_piece = db_models.SpgzPiece(**spgz_piece.dict())
    if await get_kpgz_piece_by_id(db, new_spgz_piece.kpgz_piece_id) is None:
        return None
    db.add(new_spgz_piece)
    db.commit()
    db.refresh(new_spgz_piece)
    return new_spgz_piece
