import requests
from bson import ObjectId

from tests.base_test import BaseTestClass


class BaseUser(BaseTestClass):
    def __init__(self):
        self.BASE_URL = "http://localhost:8080"
        self.session = requests.Session()
        self.session_storage = {
            "email": self.fake.email(),
            "password": self.fake.password(),
            "username": self.fake.user_name(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "date_of_birth": self.fake.date_of_birth().isoformat(),
            "post_content": self.fake.sentence(),
            "current_post_id": None,
            "user_identity": None,
        }

    def __del__(self):
        self.session.close()

    def __str__(self):
        attributes = "\n".join(
            f"{key}: {value}" for key, value in self.session_storage.items()
        )
        return attributes

    def register(self):
        url = f"{self.BASE_URL}/auth/register"
        data = {
            "first_name": self.session_storage["first_name"],
            "last_name": self.session_storage["last_name"],
            "username": self.session_storage["username"],
            "email": self.session_storage["email"],
            "password": self.session_storage["password"],
            "date_of_birth": self.session_storage["date_of_birth"],
        }
        response = self.session.post(url, json=data)

        if response.status_code != 200:
            error_message = self.buildErrorMessage(
                response.status_code, response.content
            )
            raise RuntimeError(error_message)

    def login(self):
        url = f"{self.BASE_URL}/auth/login"
        data = {
            "email": self.session_storage["email"],
            "password": self.session_storage["password"],
        }
        response = self.session.post(url, json=data)

        if response.status_code != 200:
            error_message = self.buildErrorMessage(
                response.status_code, response.content
            )
            raise RuntimeError(error_message)

    def create_post(self):
        url = f"{self.BASE_URL}/posts"
        data = {"post_content": self.session_storage["post_content"]}

        response = self.session.post(url, json=data, cookies=self.session.cookies.get_dict())
        self.session_storage["current_post_id"] = ObjectId(response.json().strip('"'))
