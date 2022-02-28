from firebase_admin import firestore

from pyruby_backend.models import User, Invite


class UserRepo(object):

    def __init__(self):
        self.db = firestore.client()

    def add_user(self, user: User):
        self.db.collection(u'users').document(user.id).set(user.dict(exclude={'id', }))

    def find_user(self, id: str):
        result = self.db.collection(u'users').document(id).get()

        return User(id=result.id, **result.to_dict())

    def add_invite(self, invite: Invite):
        self.db.collection(u'invites').document(invite.id).set(invite.dict(exclude={'id', }))
