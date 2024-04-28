import json

from tests.base_test import BaseTestClass


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
        pass

    def test_update_profile_valid(self, shared_variables, session):
        pass

    def test_update_profile_no_payload(self, shared_variables, session):
        pass

    def test_update_profile_valid_new_picture(self, shared_variables, session):
        pass

    def test_update_profile_invalid_new_picture(self, shared_variables, session):
        pass

    def test_archive_profile_valid(self, shared_variables, session):
        pass

    def test_archive_profile_no_session_token(self, shared_variables, session):
        pass

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
