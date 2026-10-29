import allure

from locators.order_page_locators import OrderPageLocators
from pages.base_page import BasePage


class OrderPage(BasePage):
    """Page Object страницы оформления заказа."""

    @allure.step("Заполнить шаг 1")
    def fill_step_1(self, data: dict):
        for key, locator in OrderPageLocators.STEP1_FIELDS.items():
            self._type(locator, data[key])

        self.select_metro_station(data["metro"])

    @allure.step("Выбрать станцию метро: {station}")
    def select_metro_station(self, station: str):
        self._click(OrderPageLocators.STEP_1_METRO_INPUT)
        self._wait_visible(
            OrderPageLocators.STEP_1_METRO_OPTIONS_LIST
        )
        self._click_text(
            OrderPageLocators.STEP_1_METRO_OPTIONS,
            station,
        )

    @allure.step("Перейти к шагу 2")
    def go_to_step_2(self):
        self._click(OrderPageLocators.NEXT_BUTTON)

    @allure.step("Выбрать первую доступную дату")
    def select_date(self):
        self._click(OrderPageLocators.STEP_2_DATE_INPUT)
        self._click_index(
            OrderPageLocators.STEP_2_DATEPICKER_DAYS,
            0,
        )
        self._wait_invisible(
            OrderPageLocators.STEP_2_DATEPICKER_OVERLAY
        )

    @allure.step("Выбрать срок аренды: {duration}")
    def select_duration(self, duration: str):
        self._click(OrderPageLocators.STEP_2_DURATION_DROPDOWN)
        self._click_text(
            OrderPageLocators.STEP_2_DURATION_OPTIONS,
            duration,
        )

    @allure.step("Выбрать цвет самоката: {color}")
    def select_color(self, color: str):
        locator = OrderPageLocators.STEP_2_COLOR_OPTIONS.get(color)
        if locator is None:
            raise ValueError(f"Неизвестный цвет самоката: {color}")

        self._click(locator)

    @allure.step("Заполнить шаг 2")
    def fill_step_2(self, data: dict):
        self.select_date()
        self.select_duration(data["duration"])
        self.select_color(data["color"])
        self._type(
            OrderPageLocators.STEP_2_COMMENT_INPUT,
            data.get("comment", ""),
        )

    @allure.step("Отправить заказ")
    def submit_order(self):
        self._click(OrderPageLocators.STEP_2_SUBMIT_BUTTON)

    @allure.step("Дождаться окна подтверждения")
    def wait_for_confirmation(self):
        self._wait_visible(
            OrderPageLocators.STEP_3_CONFIRM_DIALOG
        )

    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        self._click(
            OrderPageLocators.STEP_3_CONFIRM_YES_BUTTON
        )

    @allure.step("Получить сообщение об успешном оформлении заказа")
    def get_success_message(self) -> str:
        return self.get_text(
            OrderPageLocators.STEP_3_SUCCESS_MESSAGE
        )