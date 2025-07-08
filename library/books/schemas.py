from pydantic import BaseModel, ConfigDict


class BookPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    total_amount: int
    taken_amount: int
