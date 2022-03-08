from ariadne import convert_kwargs_to_snake_case, ObjectType
from .repositories import UserRepo
from pydantic import BaseModel
from .models import User, Invitation, Login
from uuid import uuid4
from datetime import datetime, timedelta


def resolve_user(_, info):
    return UserRepo().find_user_by_login(info.context['user']['user_id'])


@convert_kwargs_to_snake_case
def create_user(_, info, input) -> User:
    payload = CreateUserInput(**input)
    user = User(id=str(uuid4()), **payload.dict())
    UserRepo().add_user(user)
    return user


@convert_kwargs_to_snake_case
def send_invitation(_, info, input) -> Invitation:
    payload = InviteUserInput(**input)
    expiry = datetime.utcnow() + timedelta(days=2)
    invitation = Invitation(id=str(uuid4()), expiry_time=int(expiry.timestamp()), sent_by_id=info.context['user']['user_id'], **payload.dict())
    UserRepo().add_invite(invitation)
    return invitation


@convert_kwargs_to_snake_case
def accept_invitation(_, info, input) -> Login:
    payload = AcceptInvitationInput(**input)
    invite = UserRepo().accept_invite(payload.invitation_id, info.context['user']['user_id'], info.context['user']['email'])
    return Login(uid=info.context['user']['user_id'], email=info.context['user']['email'], user_id=invite.user_id)


class AcceptInvitationInput(BaseModel):
    invitation_id: str


class CreateUserInput(BaseModel):
    primary_email: str
    full_name: str


class InviteUserInput(BaseModel):
    email: str
    user_id: str


user_object = ObjectType("User")
invitation_object = ObjectType("Invitation")
login_object = ObjectType("Login")


@login_object.field("user")
def resolve_login_user(login: Login, *_):
    return UserRepo().find_user(login.user_id)


@invitation_object.field("user")
def resolve_invitation_user(invitation: Invitation, *args):
    return UserRepo().find_user(invitation.user_id)


def greet_user(_, info) -> str:
    return "Greetings, user!"


def register_resolvers(query, mutation) -> [ObjectType]:
    query.set_field("me", resolve_user)
    query.set_field('hello', greet_user)
    mutation.set_field("createUser", create_user)
    mutation.set_field("sendInvitation", send_invitation)
    mutation.set_field("acceptInvitation", accept_invitation)
    return [user_object, invitation_object, login_object]
