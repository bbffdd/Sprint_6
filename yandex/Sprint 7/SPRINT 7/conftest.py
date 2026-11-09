import pytest
import requests
import json
import random
import string

BASE_URL = "https://qa-scooter.education-services.ru/api/v1"


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def register_new_courier_and_return_login_password():
    letters = string.ascii_lowercase
    login = "".join(random.choice(letters) for _ in range(10))
    password = "".join(random.choice(letters) for _ in range(10))
    first_name = "".join(random.choice(letters) for _ in range(10))
    payload = {"login": login, "password": password, "firstName": first_name}
    response = requests.post(f"{BASE_URL}/courier", data=payload)
    if response.status_code == 201:
        return [login, password, first_name]
    return []


def generate_courier_credentials():
    """Return random courier credentials without making any API call."""
    letters = string.ascii_lowercase
    return (
        "".join(random.choice(letters) for _ in range(10)),
        "".join(random.choice(letters) for _ in range(10)),
        "".join(random.choice(letters) for _ in range(10)),
    )


def register_courier():
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()
    payload = {"login": login, "password": password, "firstName": first_name}
    response = requests.post(f"{BASE_URL}/courier", data=payload)
    if response.status_code == 201:
        return login, password, first_name
    return []


@pytest.fixture
def random_courier():
    return register_courier()


@pytest.fixture
def courier_with_login(random_courier):
    login, password, _ = random_courier
    payload = {"login": login, "password": password}
    response = requests.post(f"{BASE_URL}/courier/login", data=payload)
    courier_id = response.json().get("id")
    return login, password, courier_id


@pytest.fixture
def created_order(courier_with_login):
    login, password, courier_id = courier_with_login
    payload = {"courier": courier_id, "color": ["BLACK"]}
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/orders", data=json.dumps(payload), headers=headers)
    track = response.json().get("track")
    return track, courier_id
