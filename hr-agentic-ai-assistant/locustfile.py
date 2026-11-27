from locust import HttpUser, task, between

class HRUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def ask_hr_multi_agent(self):
        self.client.post(
            "/multi-agent",
            params={"question": "What is leave policy?"}
        )