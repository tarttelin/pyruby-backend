from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    username: str


class Invite(BaseModel):
    id: str
    invite_email: str
    person_id: str
    expiry_time: int
