from pydantic import BaseModel
from enum import Enum
from fastapi import HTTPException, status
from typing import Union


class EUserLevel(int, Enum):
    user = 1
    moderator = 2
    admin = 3


def check_user_level(level):
    if level < EUserLevel.user or level > EUserLevel.admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="no such user level")
    return level


class UserBase(BaseModel):
    email: str
    level: int


class UserEdit(BaseModel):
    id: int
    level: int


class UserCreate(UserBase):
    hashed_password: str


class UserReturn(UserBase):
    id: int

    class Config:
        orm_mode = True


class TsnPieceBase(BaseModel):
    code: str
    text: str
    price: float
    uom: str


class TsnPieceCreateWithoutSpgz(BaseModel):
    code: str
    text: str
    spgz_defined: bool
    tsn_mapping_info: str
    price: float
    uom: str


class TsnPieceReturn(TsnPieceBase):
    id: int

    class Config:
        orm_mode = True


class TsnPieceEdit(BaseModel):
    id: int
    uom: Union[str, None] = None
    code: Union[str, None] = None
    text: Union[str, None] = None
    price: Union[float, None] = None


class SnPieceEdit(BaseModel):
    id: int
    uom: Union[str, None] = None
    code: Union[str, None] = None
    text: Union[str, None] = None
    price: Union[float, None] = None


class SnPieceBase(BaseModel):
    code: str
    text: str
    price: float
    uom: str


class SnPieceCreateWithoutSpgz(BaseModel):
    code: str
    text: str
    sn_mapping_info: str
    spgz_defined: bool
    price: float
    uom: str


class SnPieceReturn(SnPieceBase):
    id: int

    class Config:
        orm_mode = True


class SpgzPieceCreate(BaseModel):
    name: Union[str, None] = None
    mapping_info: Union[str, None] = None
    okpd: Union[str, None] = None
    okpd2: str
    uom: str
    description: Union[str, None] = None
    data_id: int
    kpgz_piece_id: int


class SpgzPieceEdit(BaseModel):
    id: int
    name: Union[str, None] = None
    okpd: Union[str, None] = None
    okpd2: Union[str, None] = None
    uom: Union[str, None] = None
    description: Union[str, None] = None
    data_id: Union[int, None] = None
    kpgz_piece_id: Union[int, None] = None


class KpgzPieceReturn(BaseModel):
    name: str
    id: str

    class Config:
        orm_mode = True


class KpgzPieceEdit(BaseModel):
    id: int
    name: Union[str, None] = None


class SpgzPieceReturn(BaseModel):
    name: str
    id: int
    uom: Union[str, None] = None
    description: Union[str, None] = None
    kpgz_piece: KpgzPieceReturn
    okpd: Union[str, None] = None
    okpd2: Union[str, None] = None

    class Config:
        orm_mode = True


class KpgzPieceCreate(BaseModel):
    name: str


class Hypothesis(BaseModel):
    priority: int
    probability: float
    usage_counter: int = 0


class TsnHypothesisCreate(Hypothesis):
    tsn_piece_id: int
    spgz_piece_id: int


class HypothesisReturn(Hypothesis):
    spgz_piece: SpgzPieceReturn

    class Config:
        orm_mode = True


class SnHypothesisCreate(Hypothesis):
    sn_piece_id: int
    spgz_piece_id: int


class HypothesisReturn(BaseModel):
    priority: int
    usage_counter: int = 0
    spgz_piece: SpgzPieceReturn

    def __lt__(self, other):
        return self.priority < other.priority

    class Config:
        orm_mode = True
