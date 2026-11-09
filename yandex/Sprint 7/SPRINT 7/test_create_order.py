import pytest
import requests
import json
import allure

from conftest import BASE_URL, register_new_courier_and_return_login_password


@allure.epic("API тестирование курьерского сервиса")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Параметризация")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("color,description", [
        (["BLACK"], "черный"),
        (["GREY"], "серый"),
        (["BLACK", "GREY"], "оба цвета"),
        (None, "без цвета"),
    ])
    @allure.description("Создание заказа с различными наборами цветов")
    def test_create_order_parametrized(self, color, description):
        courier = register_new_courier_and_return_login_password()
        login, password, _ = courier
        login_payload = {"login": login, "password": password}
        login_response = requests.post(f"{BASE_URL}/courier/login", data=login_payload)
        courier_id = login_response.json()["id"]
        payload = {"courier": courier_id}
        if color is not None:
            payload["color"] = color
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{BASE_URL}/orders", data=json.dumps(payload), headers=headers)
        assert response.status_code == 201
        body = response.json()
        assert "track" in body
        assert isinstance(body["track"], int)
