import json
import random
import string
from typing import Any

import requests

BASE_URL = "https://qa-scooter.education-services.ru/api/v1"
RANDOM_STRING_LENGTH = 10
HEADERS = {"Content-Type": "application/json"}


def generate_random_string(length: int = RANDOM_STRING_LENGTH) -> str:
    """Generate a random lowercase string of given length."""
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def random_courier_payload() -> dict[str, str]:
    """Return payload for a new courier with random credentials."""
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }


def payload_string(payload: dict) -> str:
    """Serialize payload to JSON string."""
    return json.dumps(payload)


def create_courier_response() -> requests.Response:
    """POST /courier with random data, return response."""
    return requests.post(f"{BASE_URL}/courier", json=random_courier_payload())


def login_courier_response(login: str, password: str) -> requests.Response:
    """POST /courier/login, return response."""
    return requests.post(
        f"{BASE_URL}/courier/login",
        data=payload_string({"login": login, "password": password}),
        headers=HEADERS,
    )


def create_order_response(courier_id: int, color: list[str] | None = None) -> requests.Response:
    """POST /orders, return response."""
    payload = {"courier": courier_id}
    if color is not None:
        payload["color"] = color
    return requests.post(
        f"{BASE_URL}/orders",
        data=payload_string(payload),
        headers=HEADERS,
    )


def delete_courier_response(courier_id) -> requests.Response:
    """DELETE /courier/{id}, return response."""
    return requests.delete(f"{BASE_URL}/courier/{courier_id}")


def accept_order_response(courier_id: int, track: str) -> requests.Response:
    """POST /order/accept with query params, return response."""
    return requests.post(
        f"{BASE_URL}/order/accept",
        params={"courier": courier_id, "order": track},
    )


def get_order_response(number: str) -> requests.Response:
    """GET /order?number=..., return response."""
    return requests.get(f"{BASE_URL}/order", params={"number": number})


def get_orders_response(page: int = 0, limit: int = 100) -> requests.Response:
    """GET /orders, return response."""
    return requests.get(f"{BASE_URL}/orders", params={"page": page, "limit": limit})
