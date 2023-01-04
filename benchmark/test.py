import time
import random

from faker import Faker
from locust import HttpUser, task, between


PetCategory = ['DOG', 'CAT']
fake = Faker()


def create_random_pet():

    return {
        "type": random.choice(PetCategory),
        "name": fake.name()
    }

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def add_pet_and_set_appointment(self):
        pet = create_random_pet()
        response = self.client.post("/pets", json=pet)
        uid = response.json().get('id')
        self.client.post(f"/pets/{uid}/appointments")

    def on_start(self):
        self.client.post("/health")