from pydantic import BaseModel


class SignUpIn(BaseModel):
    email: str
    password: str
    level: int
