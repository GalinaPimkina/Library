from pydantic import BaseModel


class BaseBook(BaseModel):
    author: str
    title: str
    amount: int
