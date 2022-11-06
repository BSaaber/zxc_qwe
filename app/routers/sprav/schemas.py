from pydantic import BaseModel
from typing import Union, List


class TsnPieceEditIn(BaseModel):
    id: int
    code: Union[str, None] = None
    text: Union[str, None] = None
    price: Union[float, None] = None
    spgz_piece_id: Union[int, None] = None


class TsnPieceCreateIn(BaseModel):
    code: str
    text: str
    price: float
    spgz_piece_id: int
