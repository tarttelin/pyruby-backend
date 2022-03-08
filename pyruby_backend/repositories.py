from firebase_admin import firestore

from pyruby_backend.models import User, Invitation


class UserRepo(object):

    def __init__(self):
        self.db = firestore.client()

    def add_user(self, user: User):
        self.db.collection(u'users').document(user.id).set(user.dict(exclude={'id', }))

    def find_user(self, id: str) -> User:
        result = self.db.collection(u'users').document(id).get()

        return User(id=result.id, **result.to_dict())

    def find_user_by_login(self, login_uid: str):
        login = self.db.collection(u'logins').document(login_uid).get()
        result = self.db.collection(u'users').document(login.get('user_id')).get()

        return User(id=result.id, **result.to_dict())

    def add_invite(self, invite: Invitation):
        self.db.collection(u'invites').document(invite.id).set(invite.dict(exclude={'id', }))

    def accept_invite(self, invite_id, user_id, email) -> Invitation:
        invite = self.db.collection(u'invites').document(invite_id).get()
        if invite.get('email') == email:
            self.db.collection(u'logins').document(user_id).set({'user_id': invite.get('user_id'), 'email': email})
            return Invitation(id=invite.id, **invite.to_dict())
        else:
            raise Exception("User's login details do not match the invite")
