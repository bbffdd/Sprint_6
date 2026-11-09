import allure
import pytest

import data as app_data
from pages.home_page import HomePage
from pages.order_page import OrderPage


@allure.feature("FAQ")
class TestFAQ:
    @pytest.mark.parametrize(
        "idx",
        app_data.FAQ_INDICES,
        ids=[f"q{i}" for i in app_data.FAQ_INDICES],
    )
    @allure.story("Раскрытие вопроса FAQ")
    def test_faq_question_opens(self, home_page: HomePage, idx: int):
        assert home_page.open_faq_and_check(idx), (
            f"FAQ-вопрос {idx} не раскрылся"
        )


@allure.feature("Заказ самоката")
class TestOrder:
    @pytest.mark.parametrize(
        "entry_point",
        ["header", "bottom"],
        ids=["header-button", "bottom-button"],
    )
    @pytest.mark.parametrize(
        "order_data",
        app_data.ORDER_DATA,
        ids=["first-data-set", "second-data-set"],
    )
    @allure.story("Позитивный сценарий заказа")
    def test_order_success(
        self,
        home_page: HomePage,
        order_page: OrderPage,
        order_data: dict,
        entry_point: str,
    ):
        home_page.click_order_button(entry_point)

        order_page.fill_step_1(order_data)
        order_page.go_to_step_2()
        order_page.fill_step_2(order_data)
        order_page.submit_order()
        order_page.wait_for_confirmation()
        order_page.confirm_order()

        success_message = order_page.get_success_message()
        assert "Заказ оформлен" in success_message, (
            f"Не появилось сообщение об успешном оформлении заказа: "
            f"{success_message}"
        )



@allure.feature("Навигация по логотипам")
class TestLogos:
    @allure.story("Логотип Самоката ведёт на главную")
    def test_scooter_logo_navigates_home(self, home_page: HomePage):
        actual_url = home_page.click_scooter_logo()

        assert actual_url.rstrip("/") == app_data.BASE_URL.rstrip("/"), (
            f"После клика по логотипу открылась неверная страница: {actual_url}"
        )

    @allure.story("Логотип Яндекса открывает главную страницу Дзена")
    def test_yandex_logo_opens_dzen(self, home_page: HomePage):
        new_window_url = home_page.click_yandex_logo()

        assert "ya.ru" in new_window_url, (
            f"Новое окно не ведёт на Дзен: {new_window_url}"
        )

    @allure.story("У логотипа Яндекса корректный alt")
    def test_yandex_logo_text(self, home_page: HomePage):
        assert home_page.get_yandex_logo_alt() == "Yandex"
