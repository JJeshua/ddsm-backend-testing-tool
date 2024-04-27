from bson import ObjectId
import json

from tests.base_test import BaseTestClass


class TestPosts(BaseTestClass):

    def test_create_post(self, shared_variables, session):
        self.register(shared_variables, session)
        self.login(shared_variables, session)

        EXPECTED = 201
        url = f"{self.BASE_URL}/posts"
        data = {"post_content": shared_variables["post_content"]}
        response = session.post(url, json=data, cookies=session.cookies.get_dict())

        if response.status_code != EXPECTED:
            print(response.content)

        shared_variables["current_post_id"] = ObjectId(response.content.decode('utf-8').strip('"'))

        assert response.status_code == EXPECTED

    def test_create_invalid_post(self, session):
        EXPECTED = 400
        url = f"{self.BASE_URL}/posts"
        response = session.post(url, cookies=session.cookies.get_dict())

        if response.status_code != EXPECTED:
            print(response.content)

        assert response.status_code == EXPECTED

    def test_get_valid_post(self, shared_variables, session):
        EXPECTED = 200

        url = f"{self.BASE_URL}/posts/{shared_variables["current_post_id"]}"
        response = session.get(url, cookies=session.cookies.get_dict())
 
        if response.status_code != EXPECTED:
            print(response.content)

        data = json.loads(response.content)

        assert '_id' in data
        assert ObjectId(data['_id']) == shared_variables["current_post_id"] 
        assert response.status_code == EXPECTED
    
    def test_get_invalid_post(self, session):
            EXPECTED = 404

            url = f"{self.BASE_URL}/posts/invalidpostID"
            response = session.get(url, cookies=session.cookies.get_dict())

            if response.status_code != EXPECTED:
                print(response.content)
            
            assert response.status_code == EXPECTED

    def test_get_post_no_id(self, session):
            EXPECTED = 404

            url = f"{self.BASE_URL}/posts"
            response = session.get(url, cookies=session.cookies.get_dict())

            if response.status_code != EXPECTED:
                print(response.content)

            assert response.status_code == EXPECTED
