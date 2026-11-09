import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC

import data as app_data
from data import BASE_URL
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

    @allure.story("FAQ")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_faq_panel_has_content(self, home_page: HomePage):
        """Каждая раскрытая FAQ-панель содержит текст ответа."""
        for idx in app_data.FAQ_INDICES:
            home_page.open_faq_and_check(idx)
            panels = home_page.driver.find_elements(
                *HomePageLocators.FAQ_PANELS
            )
            panel_text = panels[idx].text.strip()
            assert len(panel_text) > 0, f"FAQ-панель {idx} пуста"
            # Close by clicking the button again
            buttons = home_page.driver.find_elements(*HomePageLocators.FAQ_BUTTONS)
            buttons[idx].click()

    @allure.story("FAQ")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_faq_close_on_second_click(self, home_page: HomePage, wait):
        """Повторный клик по вопросу FAQ сворачивает панель."""
        idx = 0
        home_page.open_faq_and_check(idx)
        panels = home_page.driver.find_elements(*HomePageLocators.FAQ_PANELS)
        assert panels[idx].is_displayed()
        buttons = home_page.driver.find_elements(*HomePageLocators.FAQ_BUTTONS)
        buttons[idx].click()
        wait.until(lambda d: not d.find_elements(*HomePageLocators.FAQ_PANELS)[idx].is_displayed())

    @allure.story("FAQ")
    @allure.severity(allure.severity_level.MINOR)
    def test_faq_all_buttons_visible(self, home_page: HomePage, wait):
        """Все кнопки FAQ видны на странице."""
        buttons = wait.until(
            EC.presence_of_all_elements_located(HomePageLocators.FAQ_BUTTONS)
        )
        assert len(buttons) == 8, f"Ожидается 8 кнопок, получено {len(buttons)}"
        for btn in buttons:
            assert btn.is_displayed()
            assert btn.is_enabled()


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

    @allure.story("Заказ самоката")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_order_both_entry_points(self, home_page: HomePage, order_page: OrderPage):
        """Заказ через кнопку в шапке и через кнопку внизу страницы."""
        for entry_point in ("header", "bottom"):
            home_page.click_order_button(entry_point)
            order_page.fill_user_data(app_data.ORDER_DATA[0])
            order_page.select_first_metro()
            order_page.click_next()
            order_page.select_date()
            order_page.select_duration()
            order_page.select_color(app_data.ORDER_DATA[0]["color"])
            order_page.enter_comment(app_data.ORDER_DATA[0].get("comment", ""))
            order_page.click_submit()
            order_page.wait_for_confirm_dialog()
            success_text = order_page.accept_confirmation()
            assert OrderPageLocators.SUCCESS_TEXT in success_text
            # Navigate back to clean state for next iteration
            home_page.driver.get(BASE_URL)
            HomePage(home_page.driver).dismiss_cookie()

    @allure.story("Заказ самоката")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_order_empty_comment_accepted(self, home_page: HomePage, order_page: OrderPage):
        """Заказ с пустым комментарием оформляется успешно."""
        data = app_data.ORDER_DATA[2]  # комментарий уже пустой
        home_page.click_order_button("header")
        order_page.fill_user_data(data)
        order_page.select_first_metro()
        order_page.click_next()
        order_page.select_date()
        order_page.select_duration()
        order_page.select_color(data["color"])
        order_page.enter_comment("")
        order_page.click_submit()
        order_page.wait_for_confirm_dialog()
        success_text = order_page.accept_confirmation()
        assert OrderPageLocators.SUCCESS_TEXT in success_text

    @allure.story("Заказ самоката")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_order_all_color_combinations(self, home_page: HomePage, order_page: OrderPage):
        """Заказ каждым доступным цветом завершается успешно."""
        for color in OrderPageLocators.COLOR_OPTIONS:
            home_page.click_order_button("header")
            sample = app_data.ORDER_DATA[0]
            order_page.fill_user_data({
                **sample,
                "color": color,
            })
            order_page.select_first_metro()
            order_page.click_next()
            order_page.select_date()
            order_page.select_duration()
            order_page.select_color(color)
            order_page.enter_comment("")
            order_page.click_submit()
            order_page.wait_for_confirm_dialog()
            success_text = order_page.accept_confirmation()
            assert OrderPageLocators.SUCCESS_TEXT in success_text, (
                f"Цвет {color} не прошёл"
            )
            home_page.driver.get(BASE_URL)
            HomePage(home_page.driver).dismiss_cookie()

    @allure.story("Заказ самоката")
    @allure.severity(allure.severity_level.MINOR)
    def test_order_form_fields_pre_filled(self, home_page: HomePage):
        """Поля формы отображаются после перехода на страницу заказа."""
        home_page.click_order_button("header")
        inputs = home_page.driver.find_elements(*OrderPageLocators.STEP1_INPUTS)
        assert len(inputs) >= 4, f"Ожидается >=4 полей, получено {len(inputs)}"
        for inp in inputs:
            assert inp.is_displayed()

    @allure.story("Заказ самоката")
    @allure.severity(allure.severity_level.MINOR)
    def test_metro_dropdown_first_option_selectable(self, home_page: HomePage, order_page: OrderPage):
        """Первый вариант метро открывается и выбирается."""
        home_page.click_order_button("header")
        order_page.fill_user_data(app_data.ORDER_DATA[0])
        order_page.select_first_metro()
        metro_input = home_page.driver.find_element(*OrderPageLocators.METRO_INPUT)
        assert metro_input.get_attribute("value") != "", "Станция метро не выбрана"

    @allure.story("Заказ самоката")
    @allure.severity(allure.severity_level.MINOR)
    def test_duration_dropdown_selectable(self, home_page: HomePage, order_page: OrderPage):
        """Срок аренды выбирается из дропдауна."""
        home_page.click_order_button("header")
        order_page.fill_user_data(app_data.ORDER_DATA[0])
        order_page.select_first_metro()
        order_page.click_next()
        order_page.select_date()
        order_page.select_duration()
        dropdown = home_page.driver.find_element(*OrderPageLocators.DURATION_DROPDOWN)
        assert dropdown.is_displayed()

    @allure.story("Заказ самоката")
    @allure.severity(allure.severity_level.MINOR)
    def test_comment_field_accepts_text(self, home_page: HomePage, order_page: OrderPage):
        """Поле комментария принимает произвольный текст."""
        home_page.click_order_button("header")
        order_page.fill_user_data(app_data.ORDER_DATA[0])
        order_page.select_first_metro()
        order_page.click_next()
        order_page.select_date()
        order_page.select_duration()
        order_page.select_color(app_data.ORDER_DATA[0]["color"])
        order_page.enter_comment("Тестовый длинный комментарий для проверки поля")
        comment_input = home_page.driver.find_element(*OrderPageLocators.COMMENT_INPUT)
        assert comment_input.get_attribute("value") == (
            "Тестовый длинный комментарий для проверки поля"
        )

    @allure.story("Заказ самоката")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_success_modal_contains_text(self, home_page: HomePage, order_page: OrderPage):
        """Модальное окно подтверждения содержит ключевой текст."""
        home_page.click_order_button("header")
        order_page.fill_user_data(app_data.ORDER_DATA[0])
        order_page.select_first_metro()
        order_page.click_next()
        order_page.select_date()
        order_page.select_duration()
        order_page.select_color(app_data.ORDER_DATA[0]["color"])
        order_page.enter_comment("")
        order_page.click_submit()
        order_page.wait_for_confirm_dialog()
        confirm = home_page.driver.find_element(*OrderPageLocators.CONFIRM_DIALOG)
        assert confirm.is_displayed()
        yes_btn = home_page.driver.find_element(*OrderPageLocators.CONFIRM_YES_BUTTON)
        assert yes_btn.is_displayed()
        assert yes_btn.is_enabled()
