import requests
from bson import ObjectId
from faker import Faker
import base64
import os


class BaseUser:
    def __init__(self):
        self.fake = Faker()
        self.BASE_URL = "http://localhost:8080"
        self.session = requests.Session()
        self.session_storage = {
            "email": self.fake.email(),
            "password": self.fake.password(),
            "username": self.fake.user_name(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "date_of_birth": self.fake.date_of_birth().isoformat(),
            "country": self.fake.country(),
            "biography": self.fake.paragraph(nb_sentences=3),
            "profile_picture": base64.b64encode(os.urandom(16)).decode("utf-8"),
            "post_content": self.fake.sentence(),
            "current_post_id": None,
            "current_comment_id": None,
            "comment_content": None,
            "user_identity": None,
        }

    def close_session(self):
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

    def updateProfile(self):
        url = f"{self.BASE_URL}/profile"
        data = {"profile_picture": self.session_storage["profile_picture"]}
        response = self.session.put(
            url, json=data, cookies=self.session.cookies.get_dict()
        )

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

        response = self.session.post(
            url, json=data, cookies=self.session.cookies.get_dict()
        )
        self.session_storage["current_post_id"] = ObjectId(response.json().strip('"'))

        self.session_storage["post_content"] = self.fake.sentence()

    def like_post(self, post_id):
        url = f"{self.BASE_URL}/posts/{post_id}/like"
        response = self.session.post(url, cookies=self.session.cookies.get_dict())

        if response.status_code != 201:
            error_message = self.buildErrorMessage(
                response.status_code, response.content
            )
            raise RuntimeError(error_message)

    def comment_on_post(self, post_id):
        url = f"{self.BASE_URL}/posts/{post_id}/comment"
        comment = self.fake.sentence()
        data = {"comment_content": comment}

        self.session_storage["comment_content"] = comment
        response = self.session.post(
            url, json=data, cookies=self.session.cookies.get_dict()
        )
        self.session_storage["current_comment_id"] = ObjectId(
            response.json().strip('"')
        )

        if response.status_code != 201:
            error_message = self.buildErrorMessage(
                response.status_code, response.content
            )
            raise RuntimeError(error_message)

    def buildErrorMessage(self, response_status_code, response_content):
        return f"Unexpected status code: {response_status_code}. Response content: {response_content}"

    def archive_profile(self, includeCookies):
        url = f"{self.BASE_URL}/profile/archive"
        cookies = self.session.cookies.get_dict() if includeCookies else None
        response = self.session.put(url, cookies=cookies)

    def unarchive_profile(self, includeCookies):
        url = f"{self.BASE_URL}/profile/unarchive"
        cookies = self.session.cookies.get_dict() if includeCookies else None
        response = self.session.put(url, cookies=cookies)

    def delete_profile(self, includeCookies):
        url = f"{self.BASE_URL}/profile/delete"
        cookies = self.session.cookies.get_dict() if includeCookies else None
        response = self.session.delete(url, cookies=cookies)

        return response