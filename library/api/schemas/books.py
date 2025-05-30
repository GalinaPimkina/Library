from pydantic import BaseModel


class Book(BaseModel):
    id: int
    author: str
    title: str
    amount: int
