from starlette.testclient import TestClient
from pyruby_backend import main


def test_app():
    client = TestClient(main.app)
    response = client.post("/graphql/", json={'query': '{ hello }'})
    assert response.status_code == 200
    assert "hello" in response.json()["data"].keys()


def test_user_registration_journey(admin_user, base_user):
    client = TestClient(main.app)
    create_user_gql = """
    mutation createUser($email: String!, $name: String!) {
        createUser(input: {primaryEmail: $email, fullName: $name}) {
            id
            primaryEmail
            fullName
        }
    }
    """
    user = _run_gql(client, create_user_gql, {"email": base_user['email'], "name": "Bobby McBob"}, "createUser", admin_user)
    assert user["fullName"] == "Bobby McBob"

    invite_gql = """
    mutation sendInvitation($userId: ID!, $email: String!) {
        sendInvitation(input: {userId: $userId, email: $email}) {
            id
            user {
                fullName
            }
            email
        }
    }
    """

    invitation = _run_gql(client, invite_gql, {"userId": user['id'], "email": user['primaryEmail']}, 'sendInvitation', admin_user)
    assert invitation['user']['fullName'] == 'Bobby McBob'

    accept_invitation_gql = """
        mutation acceptInvitation($invitationId: ID!) {
            acceptInvitation(input: { invitationId: $invitationId}) {
                uid
                email
                user {
                    id
                    fullName
                }
            }
        }
    """

    new_login = _run_gql(client, accept_invitation_gql, {"invitationId": invitation['id']}, 'acceptInvitation', base_user)
    assert new_login['email'] == base_user['email']

    get_me_gql = """
    query me {
        me {
            id
            fullName
            primaryEmail
        }
    }
    """
    me = _run_gql(client, get_me_gql, {"cacheBuster": base_user['localId']}, 'me', base_user)
    assert me['primaryEmail'] == base_user['email']
    assert me['fullName'] == 'Bobby McBob'


def test_only_admin_users_can_create_new_users(base_user):
    client = TestClient(main.app)
    create_user_gql = """
        mutation createUser($email: String!, $name: String!) {
            createUser(input: {primaryEmail: $email, fullName: $name}) {
                id
                primaryEmail
                fullName
            }
        }
        """
    response = client.post("/graphql/", headers={"authorization": f"Bearer {base_user['idToken']}"}, json={
        'query': create_user_gql,
        'operationName': "createUser",
        'variables': {"email": base_user['email'], "name": "Bobby McBob"}
    })
    assert response.json().get("errors") is not None
    assert response.json().get("errors")[0]["path"][0] == "createUser"


def _run_gql(client, query, args, operation, user):
    response = client.post("/graphql/", headers={"authorization": f"Bearer {user['idToken']}"}, json={
        'query': query,
        'operationName': operation,
        'variables': args
    })
    assert response.json().get("errors", None) is None
    assert response.status_code == 200
    assert response.json()["data"][operation] is not None
    return response.json()["data"][operation]
