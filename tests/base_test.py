import pytest
import requests
import random
from faker import Faker
from bson import ObjectId


class BaseTestClass:
    fake = Faker()
    BASE_URL = "http://localhost:8080"

    @pytest.fixture(scope="class")
    def session(self):
        session = requests.Session()
        yield session
        session.close()

    @pytest.fixture(scope="class")
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
            "user_identity": None,
            "limit": random.randrange(100),
            "step": 0,
        }
        return shared_data

    def register(self, shared_variables, session):
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

        if response.status_code != 200:
            error_message = self.buildErrorMessage(
                response.status_code, response.content
            )
            raise RuntimeError(error_message)

    def login(self, shared_variables, session):
        url = f"{self.BASE_URL}/auth/login"
        data = {
            "email": shared_variables["email"],
            "password": shared_variables["password"],
        }
        response = session.post(url, json=data)

        if response.status_code != 200:
            error_message = self.buildErrorMessage(
                response.status_code, response.content
            )
            raise RuntimeError(error_message)

    def create_post(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts"
        data = {"post_content": shared_variables["post_content"]}

        response = session.post(url, json=data, cookies=session.cookies.get_dict())
        shared_variables["current_post_id"] = ObjectId(response.json().strip('"'))

    def makeNewComment(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts/{shared_variables["current_post_id"]}/comment"
        data = {"comment_content": self.fake.sentence()}
        response = session.post(url, json=data,cookies=session.cookies.get_dict())
        shared_variables["current_comment_id"] = ObjectId(response.json().strip('"'))

    def buildErrorMessage(self, response_status_code, response_content):
        return f"Unexpected status code: {response_status_code}. Response content: {response_content}"
