from pydantic import BaseModel
from typing import Union, List
from app.database.schemas import HypothesisReturn


class SmetaLine(BaseModel):
    code: str = "код не распознан"
    name: str = "название работы не распознано"
    uom: str = "  "
    amount: int = 0
    price: float = 0
    hypothesises: List[HypothesisReturn] = []
    spgz_defined: bool = False

    def __lt__(self, other):
        return self.price < other.price

    line_number: int = 11


class SmetaCategory(BaseModel):
    name: str = "название раздела не распознано"
    total_price: float = 0
    lines: List[SmetaLine] = []
    key_line: SmetaLine = SmetaLine()


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
    key_lines: List[int] = []


class ParseSmetaIn(BaseModel):
    address: Union[str, None] = None
    name: Union[str, None] = None

