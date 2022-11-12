from pydantic import BaseModel
from typing import Union, List
from app.database.schemas import HypothesisReturn


class SmetaLine(BaseModel):
    code: str = "код не распознан"
    name: str = "название работы не распознано"
    uom: str = "  "
    amount: int = 123321
    price: float = 123321
    hypothesises: List[HypothesisReturn] = []
    spgz_defined: bool = False

    line_number: int = 11


class SmetaCategory(BaseModel):
    name: str = "название раздела не распознано"
    total_price: float = 0
    lines: List[SmetaLine] = []


class Smeta(BaseModel):
    address: str = "адрес не распознан"
    total_price: float = 0
    name: str = "название не распознано"
    categories: List[SmetaCategory] = []


class PatchPair(BaseModel):
    line_number: int
    spgz_id: int


class ByHandPair(BaseModel):
    line_number: int
    spgz_text: str


class PatchSmetaIn(BaseModel):
    patches: List[PatchPair] = []
    by_hand: List[ByHandPair] = []
