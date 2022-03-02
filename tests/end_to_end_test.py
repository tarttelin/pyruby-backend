from starlette.testclient import TestClient
from pyruby_backend import main


def test_app():
    client = TestClient(main.app)
    response = client.post("/graphql/", json={'query': '{ hello }'})
    assert response.status_code == 200
    assert "hello" in response.json()["data"].keys()


def test_create_user(admin_creds):
    client = TestClient(main.app)
    create_user_gql = """
    mutation createUser($email: String!, $username: String!) {
        createUser(input: {email: $email, username: $username}) {
            id
            email
            username
        }
    }
    """
    response = client.post("/graphql/", headers={"authorization": f"Bearer {admin_creds}"}, json={
        'query': create_user_gql,
        'operationName': 'createUser',
        'variables': {
            'email': "chris@me.there",
            'username': "sir_codalot"
        }
    })
    assert response.status_code == 200
    assert response.json()["data"]["createUser"]["username"] == "sir_codalot"

