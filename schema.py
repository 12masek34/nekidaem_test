import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserResponseSchema(UserSchema):
    id: int


class SubscribeSchema(BaseModel):
    user_id: int
    blog_id: int

    class Config:
        orm_mode = True


class SubscribeResponseSchema(SubscribeSchema):
    id: int


class PostSchema(BaseModel):
    id: int
    blog_id: int
    title: str
    text: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True
