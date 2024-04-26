import pytest
import requests
from faker import Faker

from constants.constants import BASE_URL


class TestAuthentication:
    fake = Faker()

    @pytest.fixture(scope="module")
    def session(self):
        session = requests.Session()
        yield session
        session.close()

    @pytest.fixture(scope="module")
    def shared_variables(self, session):
        shared_data = {
            "email": self.fake.email(),
            "password": self.fake.password(),
            "username": self.fake.user_name(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "date_of_birth": self.fake.date_of_birth().isoformat(),
        }
        return shared_data

    def test_valid_register(self, shared_variables, session):
        url = f"{BASE_URL}/auth/register"
        data = {
            "first_name": shared_variables["first_name"],
            "last_name": shared_variables["last_name"],
            "username": shared_variables["username"],
            "email": shared_variables["email"],
            "password": shared_variables["password"],
            "date_of_birth": shared_variables["date_of_birth"],
        }
        response = session.post(url, json=data)

        if response.status_code != 200:
            print("Error message:", response.content)

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "missing_field",
        ["first_name", "last_name", "username", "email", "password", "date_of_birth"],
    )
    def test_missing_register_field(self, shared_variables, session, missing_field):
        url = f"{BASE_URL}/auth/register"

        # Create data dictionary without the specified missing field
        data = {
            "first_name": (
                shared_variables["first_name"]
                if missing_field != "first_name"
                else None
            ),
            "last_name": (
                shared_variables["last_name"] if missing_field != "last_name" else None
            ),
            "username": (
                shared_variables["username"] if missing_field != "username" else None
            ),
            "email": shared_variables["email"] if missing_field != "email" else None,
            "password": (
                shared_variables["password"] if missing_field != "password" else None
            ),
            "date_of_birth": (
                shared_variables["date_of_birth"]
                if missing_field != "date_of_birth"
                else None
            ),
        }

        response = session.post(url, json=data)

        assert response.status_code == 400

    @pytest.mark.parametrize(
        "incorrect_field",
        ["first_name", "last_name", "username", "email", "password", "date_of_birth"],
    )
    def test_incorrect_register_field(self, shared_variables, session, incorrect_field):
        url = f"{BASE_URL}/auth/register"

        # Create data dictionary without the specified missing field
        data = {
            "first_name": (
                shared_variables["first_name"]
                if incorrect_field != "first_name"
                else "aa"
            ),
            "last_name": (
                shared_variables["last_name"]
                if incorrect_field != "last_name"
                else "bb"
            ),
            "username": (
                shared_variables["username"] if incorrect_field != "username" else "cc"
            ),
            "email": shared_variables["email"] if incorrect_field != "email" else None,
            "password": (
                shared_variables["password"]
                if incorrect_field != "password"
                else "12345"
            ),
            "date_of_birth": (
                shared_variables["date_of_birth"]
                if incorrect_field != "date_of_birth"
                else "aoeu"
            ),
        }

        response = session.post(url, json=data)

        assert response.status_code == 400

    def test_valid_login(self, shared_variables, session):
        url = f"{BASE_URL}/auth/login"
        data = {
            "email": shared_variables["email"],
            "password": shared_variables["password"],
        }
        response = session.post(url, json=data)

        if response.status_code != 200:
            print("Error message:", response.content)

        assert response.status_code == 200
        assert "session_token" in session.cookies
