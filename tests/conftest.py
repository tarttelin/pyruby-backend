import pytest
import requests
from requests.exceptions import HTTPError
import os


@pytest.fixture(autouse=True, scope="session")
def delete_users():
    request_url = f"http://{os.getenv('FIREBASE_AUTH_EMULATOR_HOST', 'localhost:9099')}/emulator/v1/projects/pyruby-web-home/accounts"
    resp = requests.delete(request_url)

    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise HTTPError(resp.text)

    return resp.json()


@pytest.fixture(scope="module")
def admin_user():
    data = {"email": "admin_user@example.com", "password": "password", "returnSecureToken": True}
    user = _auth_command(None, data)
    _auth_command("update", {'localId': user['localId'], 'customAttributes': '{"role": "admin"}'})
    login = _auth_command("signInWithPassword?key=dummy_key", data, headers={}, project="")

    return login


@pytest.fixture(scope="module")
def base_user():
    data = {"email": "basic_user@example.com", "password": "password", "returnSecureToken": True}
    user = _auth_command(None, data)
    _auth_command("update", {'localId': user['localId'], 'customAttributes': '{"role": "user"}'})
    login = _auth_command("signInWithPassword?key=dummy_key", data, headers={}, project="")

    return login


def _auth_command(command, payload, project="/projects/pyruby-web-home", headers={"authorization": "Bearer owner"}):
    _command = f":{command}" if command else ""
    request_url = f"http://{os.getenv('FIREBASE_AUTH_EMULATOR_HOST', 'localhost:9099')}/identitytoolkit.googleapis.com/v1{project}/accounts{_command}"

    resp = requests.post(request_url, json=payload, headers=headers)

    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise HTTPError(resp.text)

    return resp.json()