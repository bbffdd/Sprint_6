import allure
import pytest

import data as app_data
from locators.home_page_locators import HomePageLocators
from locators.order_page_locators import OrderPageLocators
from pages.home_page import HomePage
from pages.order_page import OrderPage


@allure.feature("FAQ")
class TestFAQ:
    """Тесты «Часто задаваемых вопросов»."""

    @pytest.mark.parametrize(
        "idx",
        app_data.FAQ_INDICES,
        ids=[f"q{i}" for i in app_data.FAQ_INDICES],
    )
    @allure.story("Раскрытие вопроса FAQ")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_faq_question_opens(self, home_page: HomePage, idx: int):
        assert home_page.open_faq_and_check(idx), (
            f"FAQ-вопрос {idx} не раскрыт"
        )


@allure.feature("Заказ самоката")
class TestOrder:
    """Тесты сценария заказа самоката."""

    @pytest.mark.parametrize(
        "data",
        app_data.ORDER_DATA,
        ids=["ivanov", "petrova", "sidorov"],
    )
    @allure.story("Позитивный сценарий заказа")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_order_success(
        self,
        home_page: HomePage,
        order_page: OrderPage,
        data: dict,
    ):
        home_page.click_order_button("header")

        order_page.fill_user_data(data)
        order_page.select_first_metro()
        order_page.click_next()

        order_page.select_date()
        order_page.select_duration()
        order_page.select_color(data["color"])
        order_page.enter_comment(data.get("comment", ""))

        order_page.click_submit()
        order_page.wait_for_confirm_dialog()
        success_text = order_page.accept_confirmation()

        assert OrderPageLocators.SUCCESS_TEXT in success_text

    @allure.story("Навигация по логотипам")
    @allure.severity(allure.severity_level.MINOR)
    def test_scooter_logo_navigates_home(self, home_page: HomePage):
        home_page.click_scooter_logo()

        assert (
            HomePageLocators.SCOOTER_HOME_URL
            in home_page.get_current_url()
        )

    @allure.story("Навигация по логотипам")
    @allure.severity(allure.severity_level.MINOR)
    def test_yandex_logo_opens_new_window(self, home_page: HomePage):
        new_window_url = home_page.click_yandex_logo()

        assert new_window_url.startswith("https://ya.ru"), (
            f"Новое окно не ведёт на Яндекс. URL: {new_window_url}"
        )

    @allure.story("Навигация по логотипам")
    @allure.severity(allure.severity_level.MINOR)
    def test_yandex_logo_text(self, home_page: HomePage):
        assert home_page.get_yandex_logo_alt() == "Yandex"
