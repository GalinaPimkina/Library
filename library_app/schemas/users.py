from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username: str
    is_active: bool


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    pass