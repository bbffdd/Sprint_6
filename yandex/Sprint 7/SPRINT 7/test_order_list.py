import requests
import allure

from conftest import BASE_URL


@allure.epic("API тестирование курьерского сервиса")
@allure.feature("Список заказов")
class TestOrderList:

    @allure.story("Позитивный сценарий")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Проверка: список заказов возвращается 200, orders - массив, есть pageInfo")
    def test_order_list_returns_list(self):
        response = requests.get(f"{BASE_URL}/orders", params={"page": 1, "limit": 5})
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body.get("orders"), list)
        page_info = body.get("pageInfo", {})
        assert "page" in page_info
        assert "total" in page_info
        assert "limit" in page_info
