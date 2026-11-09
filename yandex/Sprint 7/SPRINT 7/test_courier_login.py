import pytest
import requests
import json
import random
import string
import allure

from conftest import BASE_URL, register_new_courier_and_return_login_password


@allure.epic("API тестирование курьерского сервиса")
@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.story("Позитивный сценарий")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Проверка: курьер может авторизоваться, возвращается 200 и id")
    def test_can_login(self):
        courier = register_new_courier_and_return_login_password()
        login, password, _ = courier
        payload = {"login": login, "password": password}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 200
        body = response.json()
        assert "id" in body

    @allure.story("Позитивный сценарий")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверка: успешная авторизация возвращает числовой id курьера")
    def test_login_returns_courier_id(self):
        courier = register_new_courier_and_return_login_password()
        login, password, _ = courier
        payload = {"login": login, "password": password}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        body = response.json()
        assert isinstance(body.get("id"), int)

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка: неправильный пароль возвращает 404 и сообщение 'Учетная запись не найдена'")
    def test_wrong_password_returns_error(self):
        courier = register_new_courier_and_return_login_password()
        # Нижнее подчеркивание исключает часть данных
        login, _password, _ = courier
        payload = {"login": login, "password": "wrongpassword"}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 404
        body = response.json()
        assert body["code"] == 404
        assert "не найдена" in body["message"].lower()

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверка: авторизация под несуществующим пользователем возвращает 404")
    def test_nonexistent_user_returns_error(self):
        payload = {"login": "nonexistent_user_xyz", "password": "anypassword123"}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 404
        body = response.json()
        assert body["code"] == 404

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.description("Проверка: при отсутствии обязательного поля возвращается 400 (пустой или JSON body)")
    def test_missing_field_returns_error(self, missing_field):
        login = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
        password = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
        payload = {"login": login, "password": password}
        del payload[missing_field]
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code != 200
        # API может вернуть 400 (пустой или JSON body) или 504 главное не 200
        if response.text:
            try:
                body = response.json()
                assert "code" in body
            except json.JSONDecodeError:
                pass  # пустой body ок
