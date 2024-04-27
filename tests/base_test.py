import pytest
import requests
from faker import Faker


class BaseTestClass:
    fake = Faker()
    BASE_URL = "http://localhost:8080"

    @pytest.fixture(scope="module")
    def session(self):
        session = requests.Session()
        yield session
        session.close()

    @pytest.fixture(scope="module")
    def shared_variables(self):
        shared_data = {
            "email": self.fake.email(),
            "password": self.fake.password(),
            "username": self.fake.user_name(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "date_of_birth": self.fake.date_of_birth().isoformat(),
            "post_content": self.fake.sentence(),
            "current_post_id": None,
        }
        return shared_data

    def register(self, shared_variables, session):
        EXPECTED = 200
        url = f"{self.BASE_URL}/auth/register"
        data = {
            "first_name": shared_variables["first_name"],
            "last_name": shared_variables["last_name"],
            "username": shared_variables["username"],
            "email": shared_variables["email"],
            "password": shared_variables["password"],
            "date_of_birth": shared_variables["date_of_birth"],
        }
        response = session.post(url, json=data)

        if response.status_code != EXPECTED:
            print(response.content)

    def login(self, shared_variables, session):
        EXPECTED = 200
        url = f"{self.BASE_URL}/auth/login"
        data = {
            "email": shared_variables["email"],
            "password": shared_variables["password"],
        }
        response = session.post(url, json=data)

        if response.status_code != EXPECTED:
            print(response.content)

    def buildErrorMessage(self, response_status_code, response_content):
        return f"Unexpected status code: {response_status_code}. Response content: {response_content}"    