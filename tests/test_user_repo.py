from pyruby_backend.repositories import UserRepo
from pyruby_backend.models import User


def test_store_new_user():
    repo = UserRepo()
    expected = User(id="123", email="foo@bar.com", username="bob")
    repo.add_user(expected)
    actual = repo.find_user(expected.id)
    assert expected.email == actual.email
