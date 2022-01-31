from firebase_admin import firestore


def resolve_user(_, info):
    db = firestore.client()
    users_ref = db.collection(u'users').document(info.context['user']['uid'])
    return users_ref.get()
