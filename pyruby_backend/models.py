from pydantic import BaseModel


class User(BaseModel):
    id: str
    primary_email: str
    full_name: str


class Invitation(BaseModel):
    id: str
    email: str
    user_id: str
    expiry_time: int
    sent_by_id: str


class Login(BaseModel):
    uid: str
    email: str
    user_id: str
