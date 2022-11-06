from pydantic import BaseModel
from typing import Union, List
from app.database.schemas import HypothesisReturn


class SmetaLine(BaseModel):
    # userful info
    code: str = "DEFAULT CODE"
    name: str = "DEFAULT NAME"
    uom: str = "DEFAULT UOM"
    amount: int = 123321
    price: float = 123321
    hypothesises: List[HypothesisReturn] = []
    spgz_defined: bool = False

    line_number: int = 11


class SmetaCategory(BaseModel):
    name: str = "DEFAULT CATEGORY NAME"
    lines: List[SmetaLine] = []


class Smeta(BaseModel):
    address: str = "DEFAULT ADDRESS"
    categories: List[SmetaCategory] = []


class PatchPair(BaseModel):
    line_number: int
    spgz_id: int


class PatchSmetaIn(BaseModel):
    patches: List[PatchPair] = []
