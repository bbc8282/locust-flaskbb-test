import time
import random
from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    host = "http://myflaskbb.org:5000"  # FlaskBB가 실행되는 주소
    #wait_time = between(0.01, 0.05)
    created_topic_ids = []

    @task(0)
    def create_user(self):
        random_number = random.randint(1, 50000)
        username = f"testuser-{random_number}"
        password = f"password-{random_number}"
        email = f"test-{random_number}@example.com"
        group_id = 4

        response = self.client.post(f"/api/users/{username}", json={
            "password": password,
            "email": email,
            "group_id": group_id
        })

    @task(0)
    def delete_user(self):
        random_number = random.randint(1, 50000)
        username = f"testuser-{random_number}"
        
        response = self.client.delete(f"/api/users/{username}")

        if response.status_code != 200 and response.status_code != 404:
            print(f"Failed to delete user {username}. Status code: {response.status_code}")

    @task(1)
    def create_topic(self):
        title = "Test Title" + str(random.randint(1, 50000))
        content = f"![https://w7.pngwing.com/pngs/869/485/png-transparent-google-logo-computer-icons-google-text-logo-google-logo-thumbnail.png](url)"
        forum_id = 1
        user_id = 1

        response = self.client.post("/api/forums/topics-test", json={
            "title": title,
            "content": content,
            "forum_id": forum_id,
            "user_id": user_id
        })

        #if response.status_code == 201:
        #    topic_data = response.json()
        #    topic_id = topic_data.get('topic_id')  # post id를 추출
        #    self.created_topic_ids.append(topic_id)
        #else:
        #    print(f"Failed to create topic. Status code: {response.status_code}")


    @task(0)
    def delete_topic(self):
        if self.created_topic_ids:
            topic_id_to_delete = self.created_topic_ids.pop()
            if topic_id_to_delete is not None:
                response = self.client.delete(f"/api/forums/topics/{topic_id_to_delete}")

            if response.status_code != 201:  # 삭제 성공 시의 상태 코드가 201로 가정
                print(f"Failed to delete topic with id {topic_id_to_delete}. Status code: {response.status_code}")

    #def on_stop(self):
    #    response = self.client.delete("/api/delete_all_users")
    #    response = self.client.delete("/api/delete_all_topics")