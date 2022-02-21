from .repositories import UserRepo
from pydantic import BaseModel
from .models import User
from uuid import uuid4


def resolve_user(_, info):
    return UserRepo().find_user(info.context['user']['id'])


def create_user(_, info, input) -> User:
    payload = CreateUserInput(**input)
    user = User(id=str(uuid4()), **payload.dict())
    UserRepo().add_user(user)
    return user


class CreateUserInput(BaseModel):
    email: str
    username: str


def greet_user(_, info) -> str:
    return "Greetings, user!"


def register_resolvers(query, mutation):
    query.set_field("me", resolve_user)
    query.set_field('hello', greet_user)
    mutation.set_field("createUser", create_user)
