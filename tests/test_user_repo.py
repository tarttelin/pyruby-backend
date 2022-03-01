from pyruby_backend.repositories import UserRepo
from pyruby_backend.models import User
import requests
from requests.exceptions import HTTPError
import os

def test_store_new_user():
    repo = UserRepo()
    expected = User(id="123", email="foo@bar.com", username="bob")
    repo.add_user(expected)
    actual = repo.find_user(expected.id)
    assert expected.email == actual.email


def test_login():
    data = {"email": "chris@tarttelin.co.uk", "password": "password", "returnSecureToken": True}
    _auth_command("signUp", data)
    login = _auth_command("signInWithPassword", data)

    print(login)


def _auth_command(command, payload):
    request_url = f"http://{os.getenv('FIREBASE_AUTH_EMULATOR_HOST', 'firebase:9099')}/identitytoolkit.googleapis.com/v1/accounts:{command}?key=dummy_key"

    resp = requests.post(request_url, json=payload)

    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise HTTPError(e, resp.text)

    return resp.json()
