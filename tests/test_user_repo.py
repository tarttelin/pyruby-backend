import pytest

from pyruby_backend.repositories import UserRepo
from pyruby_backend.models import User
import requests
from requests.exceptions import HTTPError
import os
from starlette.testclient import TestClient
from pyruby_backend import main


@pytest.fixture
def user_repo():
    client = TestClient(main.app)
    return UserRepo()


def test_store_new_user(user_repo):
    expected = User(id="123", primary_email="foo@bar.com", full_name="bob")
    user_repo.add_user(expected)
    actual = user_repo.find_user(expected.id)
    assert expected.primary_email == actual.primary_email


def test_login():
    data = {"email": "chris@tarttelin.co.uk", "password": "password", "returnSecureToken": True}
    result = _auth_command("signUp", data)
    login = _auth_command("signInWithPassword", data)

    assert login['email'] == data['email']


def _auth_command(command, payload):
    request_url = f"http://{os.getenv('FIREBASE_AUTH_EMULATOR_HOST', 'localhost:9099')}/identitytoolkit.googleapis.com/v1/accounts:{command}?key=dummy_key"

    resp = requests.post(request_url, json=payload)

    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise HTTPError(e, resp.text)

    return resp.json()
