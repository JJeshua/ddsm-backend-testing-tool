import pytest

from tests.base_test import BaseTestClass


class TestAuthentication(BaseTestClass):
    def test_register_valid(self, shared_variables, session):
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

        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_register_duplicate_user(self, shared_variables, session):
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

        assert response.status_code == 400, self.buildErrorMessage(
            response.status_code, response.content
        )

    @pytest.mark.parametrize(
        "missing_field",
        ["first_name", "last_name", "username", "email", "password", "date_of_birth"],
    )
    def test_register_missing_field(self, shared_variables, session, missing_field):
        url = f"{self.BASE_URL}/auth/register"

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

        assert response.status_code == 400, self.buildErrorMessage(
            response.status_code, response.content
        )

    @pytest.mark.parametrize(
        "incorrect_field",
        ["first_name", "last_name", "username", "email", "password", "date_of_birth"],
    )
    def test_register_incorrect_field(self, shared_variables, session, incorrect_field):
        url = f"{self.BASE_URL}/auth/register"

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

        assert response.status_code == 400, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_login_invalid(self, shared_variables, session):
        url = f"{self.BASE_URL}/auth/login"
        data = {
            "email": shared_variables["email"],
            "password": f"{shared_variables["password"]}aoeuu",
        }
        response = session.post(url, json=data)

        assert response.status_code == 400, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_login_valid(self, shared_variables, session):
        url = f"{self.BASE_URL}/auth/login"
        data = {
            "email": shared_variables["email"],
            "password": shared_variables["password"],
        }
        response = session.post(url, json=data)

        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )
        assert "session_token" in session.cookies, self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_is_authenticated(self, session):
        url = f"{self.BASE_URL}/auth/isAuthenticated"
        response = session.get(url, cookies=session.cookies.get_dict())

        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )
        assert "session_token" in session.cookies, self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_session_token_no_session_token(self, session):
        url = f"{self.BASE_URL}/auth/isAuthenticated"
        response = session.get(url)

        assert response.status_code == 403, self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_session_token_invalid(self, session):
        url = f"{self.BASE_URL}/auth/isAuthenticated"
        response = session.get(url, cookies={"session_token":"idksomethinginvalid"})

        assert response.status_code == 403, self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_logout(self, session):
        url = f"{self.BASE_URL}/auth/logout"
        response = session.get(url, cookies=session.cookies.get_dict())

        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )
    

    def test_session_token_invalidated(self, session):
        url = f"{self.BASE_URL}/auth/isAuthenticated"
        response = session.get(url, cookies=session.cookies.get_dict())

        assert response.status_code == 403, self.buildErrorMessage(
            response.status_code, response.content
        )
