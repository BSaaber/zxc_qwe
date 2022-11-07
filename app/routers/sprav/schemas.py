from pydantic import BaseModel


class TsnPieceCreateIn(BaseModel):
    code: str
    text: str
    price: float
    spgz_piece_id: int
