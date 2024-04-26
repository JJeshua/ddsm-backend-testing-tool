import pytest
import requests
from faker import Faker


class TestAuthentication:
    fake = Faker()
    BASE_URL = "http://localhost:8080"

    @pytest.fixture(scope="module")
    def session(self):
        session = requests.Session()
        yield session
        session.close()

    @pytest.fixture(scope="module")
    def shared_variables(self, session):
        shared_data = {
            "BASE_URL": self.BASE_URL,
            "email": self.fake.email(),
            "password": self.fake.password(),
            "username": self.fake.user_name(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "date_of_birth": self.fake.date_of_birth().isoformat(),
        }
        return shared_data

    def test_register(self, shared_variables, session):
        url = f"{shared_variables['BASE_URL']}/auth/register"
        data = {
            "username": shared_variables["username"],
            "email": shared_variables["email"],
            "password": shared_variables["password"],
            "first_name": shared_variables["first_name"],
            "last_name": shared_variables["last_name"],
            "date_of_birth": shared_variables["date_of_birth"],
        }
        response = session.post(url, json=data)

        if response.status_code != 200:
            print("Error message:", response.content)

        assert response.status_code == 200

    def test_login(self, shared_variables, session):
        url = f"{shared_variables['BASE_URL']}/auth/login"
        data = {
            "email": shared_variables["email"],
            "password": shared_variables["password"],
        }
        response = session.post(url, json=data)

        if response.status_code != 200:
            print("Error message:", response.content)

        assert response.status_code == 200
        assert "session_token" in session.cookies
