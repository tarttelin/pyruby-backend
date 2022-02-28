from pyruby_backend.repositories import UserRepo
from pyruby_backend.models import User
import requests
from requests.exceptions import HTTPError
import json

def test_store_new_user():
    repo = UserRepo()
    expected = User(id="123", email="foo@bar.com", username="bob")
    repo.add_user(expected)
    actual = repo.find_user(expected.id)
    assert expected.email == actual.email


def test_login():
    request_url = "http://localhost:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=dummy_key"
    data = {"email": "chris@tarttelin.co.uk", "password": "password", "returnSecureToken": True}

    resp = requests.post(request_url, json=data)

    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise HTTPError(e, resp.text)

    print(resp.json())
