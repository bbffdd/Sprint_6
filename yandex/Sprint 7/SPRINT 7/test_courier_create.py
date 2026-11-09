import pytest
import requests
import json
import random
import string
import allure

from conftest import BASE_URL, register_new_courier_and_return_login_password, generate_courier_credentials


@allure.epic("API тестирование курьерского сервиса")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.story("Позитивный сценарий")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Проверка: курьера можно создать, возвращается 201 и ok=true")
    def test_can_create_courier(self):
        login, password, first_name = generate_courier_credentials()
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        body = response.json()
        assert body["ok"] is True, f"Expected ok=true, got: {body}"

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка: повторная регистрация того же логина возвращает 409")
    def test_cannot_create_duplicate_login(self):
        courier = register_new_courier_and_return_login_password()
        login, password, first_name = courier
        # endpoint /courier принимает form-encoded данные (не JSON) заголовок не нужен

        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        assert response.status_code == 409
        body = response.json()
        assert body["code"] == 409

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.description("Проверка: при отсутствии обязательного поля возвращается 400 с сообщением об ошибке")
    def test_missing_required_field_returns_error(self, missing_field):
        courier = register_new_courier_and_return_login_password()
        login, password, first_name = courier
        payload = {"login": login, "password": password, "firstName": first_name}
        del payload[missing_field]
        # endpoint /courier принимает form-encoded данные заголовок не нужен
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        assert response.status_code == 400
        body = response.json()
        assert body["code"] == 400

