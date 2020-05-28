import random

from locust import HttpUser, task, between


class TestUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def create_account(self):
        with self.client.post(
            '/accounts',
            json={
                'num': random.randint(1001, 10000),
                'amount': random.randint(0, 1000),
            },
            catch_response=True,
        ) as response:
            response_json = response.json()

            if response.status_code == 400 and response_json.get('success') is False:
                response.success()

    @task(5)
    def get_account(self):
        num = random.randint(1, 1000)
        self.client.get(f'/accounts/{num}')

    @task(100)
    def transfer_amount(self):
        with self.client.post(
            '/transfer',
            json={
                'num_to': random.randint(1, 1000),
                'num_from': random.randint(1, 1000),
                'amount': random.randint(1, 10),
            },
            catch_response=True,
        ) as response:
            response_json = response.json()

            if response.status_code == 400 and response_json.get('success') is False:
                response.success()
