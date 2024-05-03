from bson import ObjectId
import json
import math

from tests.base_test import BaseTestClass


class TestPosts(BaseTestClass):
    def test_create_post(self, shared_variables, session):
        self.register(shared_variables, session)
        self.login(shared_variables, session)

        url = f"{self.BASE_URL}/posts"
        data = {"post_content": shared_variables["post_content"]}

        response = session.post(url, json=data, cookies=session.cookies.get_dict())
        shared_variables["current_post_id"] = ObjectId(response.json().strip('"'))

        assert response.status_code == 201, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_create_post_invalid_post_content(self, session):
        url = f"{self.BASE_URL}/posts"
        response = session.post(url, cookies=session.cookies.get_dict())
        assert response.status_code == 400, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_get_post_valid(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts/{shared_variables['current_post_id']}"
        response = session.get(url, cookies=session.cookies.get_dict())
        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )

        data = response.json()
        assert "_id" in data, self.buildErrorMessage(
            response.status_code, response.content
        )
        assert (
            ObjectId(data["_id"]) == shared_variables["current_post_id"]
        ), self.buildErrorMessage(response.status_code, response.status_code)

    def test_get_post_invalid(self, session):
        url = f"{self.BASE_URL}/posts/invalidpostID"
        response = session.get(url, cookies=session.cookies.get_dict())
        assert response.status_code == 404, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_get_post_no_id(self, session):
        url = f"{self.BASE_URL}/posts"
        response = session.get(url, cookies=session.cookies.get_dict())
        assert response.status_code == 404, self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_like_post(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts/{shared_variables["current_post_id"]}/like"
        response = session.post(url, cookies=session.cookies.get_dict())
        assert response.status_code == 201, self.buildErrorMessage(
            response.status_code, response.content
        )


    def test_like_post_double_like(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts/{shared_variables["current_post_id"]}/like"
        response = session.post(url, cookies=session.cookies.get_dict())
        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )


    def test_like_post_invalid_post_id(self, session):
        url = f"{self.BASE_URL}/posts/invalidpostid/like"
        response = session.post(url, cookies=session.cookies.get_dict())
        assert response.status_code == 404, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_update_post_valid(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts/{shared_variables["current_post_id"]}"
        new_content = {"post_content": self.fake.sentence()}

        response = session.put(url, json=new_content, cookies=session.cookies.get_dict())

        assert response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )
        
        url = f"{self.BASE_URL}/posts/{shared_variables['current_post_id']}"
        response = session.get(url, cookies=session.cookies.get_dict())

        content = json.loads(response.content)

        assert content["post_content"] != shared_variables["post_content"], self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_update_post_no_content(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts/{shared_variables["current_post_id"]}"

        response = session.put(url, cookies=session.cookies.get_dict())

        assert response.status_code == 400, self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_update_post_invalid_post_id(self, session):
        url = f"{self.BASE_URL}/posts/invalidPostId"

        response = session.put(url, cookies=session.cookies.get_dict())

        assert response.status_code == 404, self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_create_comment_valid(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts/{shared_variables["current_post_id"]}/comment"
        data = {"comment_content": self.fake.sentence()}
        response = session.post(url, json=data,cookies=session.cookies.get_dict())

        assert response.status_code == 201, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_create_comment_no_content(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts/{shared_variables["current_post_id"]}/comment"
        response = session.post(url, cookies=session.cookies.get_dict())

        assert response.status_code == 400, self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_create_comment_invalid_post_id(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts/invalidPostId/comment"
        response = session.post(url, cookies=session.cookies.get_dict())

        assert response.status_code == 404, self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_delete_comment_valid(self, shared_variables, session):   
        pass

    def test_delete_comment_invalid_comment_id(self, shared_variables, session):   
        pass

    def test_delete_comment_not_comment_owner(self, shared_variables, session):   
        pass
    
    def test_archive_post_valid(self, shared_variables, session):   
        pass

    def test_archive_post_invalid_post_id(self, shared_variables, session):   
        pass

    def test_archive_post_not_post_owner(self, shared_variables, session):   
        pass

    def test_unarchive_post_valid(self, shared_variables, session):   
        pass

    def test_unarchive_post_invalid_post_id(self, shared_variables, session):   
        pass

    def test_unarchive_post_not_post_owner(self, shared_variables, session):   
        pass

    def test_get_likes_valid(self, shared_variables, session):
        url = f"{self.BASE_URL}/posts/{shared_variables['current_post_id']}/{shared_variables['limit']}/{shared_variables['step']}/likes"
        response = session.get(url, cookies=session.cookies.get_dict())
        # print(response.json()[0])
        # print(response.json()[0]['username'])
        assert response.json()[0]['username'] and response.status_code == 200, self.buildErrorMessage(
            response.status_code, response.content
        )

    def test_get_likes_invalid_post_id(self, shared_variables, session):   
        url = f"{self.BASE_URL}/posts/invalidPostId/{shared_variables['limit']}/{shared_variables['step']}/likes"
        response = session.post(url, cookies=session.cookies.get_dict())
        assert response.status_code == 404, self.buildErrorMessage(
            response.status_code, response.content
        )
    
    def test_get_likes_invalid_lim(self, shared_variables, session):
        limit = -4;   
        url = f"{self.BASE_URL}/posts/{shared_variables['current_post_id']}/{limit}/{shared_variables['step']}/likes"
        response = session.get(url, cookies=session.cookies.get_dict())
        assert (not math.isnan(limit) or not (limit > 0)) \
            and (response.status_code == 400), self.buildErrorMessage(
                response.status_code, response.content
        )

    def test_get_likes_invalid_step(self, shared_variables, session):   
        step = -4;   
        url = f"{self.BASE_URL}/posts/{shared_variables['current_post_id']}/{shared_variables['limit']}/{step}/likes"
        response = session.get(url, cookies=session.cookies.get_dict())
        assert (not math.isnan(step) or not (step >= 0)) \
            and (response.status_code == 400), self.buildErrorMessage(
                response.status_code, response.content
        )

    def test_get_comments_valid(self, shared_variables, session):   
        pass

    def test_get_commments_invalid_post_id(self, shared_variables, session):   
        pass
    
    def test_get_commments_invalid_lim(self, shared_variables, session):   
        pass

    def test_get_commments_invalid_step(self, shared_variables, session):   
        pass

    def test_delete_post_valid(self, shared_variables, session):   
        pass

    def test_delete_post_invalid_post_id(self, shared_variables, session):   
        pass

    def test_delete_post_not_post_owner(self, shared_variables, session):   
        pass
