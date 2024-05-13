import json
import base64

from tests.base_test import BaseTestClass
from tests.base_user import BaseUser


class TestProfile(BaseTestClass):
    def test_get_profile_valid(self, shared_variables, session):
        self.register(shared_variables, session)
        self.login(shared_variables, session)

        url = f"{self.BASE_URL}/profile"
        data = {"post_content": shared_variables["post_content"]}

        response = session.get(url, json=data, cookies=session.cookies.get_dict())

        shared_variables["user_identity"] = json.loads(response.content)

        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )
        assert response.content != None, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_get_profile_invalid_session_token(self, shared_variables, session):
        url = f"{self.BASE_URL}/profile"
        data = {"post_content": shared_variables["post_content"]}

        response = session.get(url, json=data)

        assert response.status_code == 403, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_update_profile_valid(self, shared_variables, session):
        user = BaseUser()
        user.register()
        user.login()
        url = f"{self.BASE_URL}/profile"
        new_user_info = {
            "email": self.fake.email(),
            "username": self.fake.user_name(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "date_of_birth": self.fake.date_of_birth().isoformat(),
            "country": self.fake.country(),
            "biography": self.fake.paragraph(nb_sentences=3),
            "profile_picture": "fake-base64-string",
        }
        response = session.put(
            url, json=new_user_info, cookies=session.cookies.get_dict()
        )
        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )
        url = f"{self.BASE_URL}/profile"
        response = session.get(url, cookies=session.cookies.get_dict())
        info = json.loads(response.content)
        assert (
            info["profile"]["email"] != user.session_storage["email"]
            and info["profile"]["username"] != user.session_storage["username"]
            and info["profile"]["user_info"]["first_name"]
            != user.session_storage["first_name"]
            and info["profile"]["user_info"]["last_name"]
            != user.session_storage["last_name"]
            and info["profile"]["user_info"]["date_of_birth"]
            != user.session_storage["date_of_birth"]
            and info["profile"]["user_info"]["country"]
            != user.session_storage["country"]
            and info["profile"]["user_info"]["profile_picture"]
            != user.session_storage["profile_picture"]
        ), self.buildErrorMessage(response.status_code, response.content)

    def test_update_profile_no_payload(self, shared_variables, session):
        url = f"{self.BASE_URL}/profile"
        new_user_info = {}
        response = session.put(
            url, json=new_user_info, cookies=session.cookies.get_dict()
        )
        assert response.status_code == 400, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_update_profile_valid_new_picture(self, shared_variables, session):
        url = f"{self.BASE_URL}/profile"
        new_user_info = {
            "profile_picture": "bmV3IHByb2ZpbGUgcGljdHVyZSB0ZXN0",
        }
        if (
            base64.b64encode(base64.b64decode(new_user_info["profile_picture"])).decode(
                "utf-8"
            )
            == new_user_info["profile_picture"]
        ):
            response = session.put(
                url, json=new_user_info, cookies=session.cookies.get_dict()
            )
        else:
            assert False

        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_update_profile_invalid_new_picture(self, shared_variables, session):
        url = f"{self.BASE_URL}/profile"
        new_user_info = {
            "profile_picture": "()bmV3IHByb2ZpbGUgcGljdHVyZSB0ZXN0",
        }
        response = session.put(
            url, json=new_user_info, cookies=session.cookies.get_dict()
        )
        assert (
            base64.b64encode(base64.b64decode(new_user_info["profile_picture"])).decode(
                "utf-8"
            )
            != new_user_info["profile_picture"]
        ), self.buildErrorMessage(response.status_code, response.content)

    def test_archive_profile_valid(self, shared_variables, session):
        url = f"{self.BASE_URL}/profile/archive"
        response = session.put(url, cookies=session.cookies.get_dict())
        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_archive_profile_no_session_token(self, shared_variables, session):
        url = f"{self.BASE_URL}/profile/archive"
        response = session.put(url)
        assert response.status_code == 403, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_unarchive_profile_valid(self, shared_variables, session):
        pass

    def test_unarchive_profile_no_session_token(self, shared_variables, session):
        pass

    def test_delete_profile_valid(self, shared_variables, session):
        pass

    def test_delete_profile_no_session_token(self, shared_variables, session):
        pass

    def test_delete_profile_delete_unarchived_profile(self, shared_variables, session):
        pass
