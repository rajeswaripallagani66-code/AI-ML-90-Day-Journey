from locust import HttpUser, task
class HRUser(HttpUser):
    @task
    def chat(self):
        self.client.post("/chat", json={"message": "What is leave policy?", "user_id": "test"})