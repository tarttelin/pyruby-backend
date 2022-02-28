from ariadne import convert_kwargs_to_snake_case, ObjectType

from .repositories import UserRepo
from pydantic import BaseModel
from .models import User, Invite
from uuid import uuid4


def resolve_user(_, info):
    return UserRepo().find_user(info.context['user']['id'])


def create_user(_, info, input) -> User:
    payload = CreateUserInput(**input)
    user = User(id=str(uuid4()), **payload.dict())
    UserRepo().add_user(user)
    return user


@convert_kwargs_to_snake_case
def send_invite(_, info, input) -> Invite:
    payload = InviteUserInput(**input)
    invite = Invite(id=str(uuid4()), **payload.dict())
    UserRepo().add_invite(invite)
    return invite


class CreateUserInput(BaseModel):
    email: str
    username: str


class InviteUserInput(BaseModel):
    invite_email: str
    user_id: str


user = ObjectType("User")


def greet_user(_, info) -> str:
    return "Greetings, user!"


def register_resolvers(query, mutation) -> [ObjectType]:
    query.set_field("me", resolve_user)
    query.set_field('hello', greet_user)
    mutation.set_field("createUser", create_user)
    mutation.set_field("sendInvite", send_invite)
    return [user]
