import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from locators.order_page_locators import OrderPageLocators
from pages.base_page import BasePage


class OrderPage(BasePage):
    """Page Object страницы оформления заказа."""

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Заполнить данные пользователя")
    def fill_user_data(self, data: dict):
        self.wait.until(
            EC.visibility_of_element_located(OrderPageLocators.STEP1_FORM)
        )
        inputs = self.wait.until(
            EC.presence_of_all_elements_located(
                OrderPageLocators.STEP1_INPUTS
            )
        )

        for element in inputs:
            placeholder = element.get_attribute("placeholder")
            key = OrderPageLocators.STEP1_PLACEHOLDERS.get(placeholder)

            if key and key in data:
                element.send_keys(data[key])

    @allure.step("Выбрать первую станцию метро")
    def select_first_metro(self):
        self.wait.until(
            EC.element_to_be_clickable(OrderPageLocators.METRO_INPUT)
        ).click()
        self.wait.until(
            EC.visibility_of_element_located(
                OrderPageLocators.METRO_OPTIONS_LIST
            )
        )
        self.wait.until(
            EC.element_to_be_clickable(
                OrderPageLocators.METRO_FIRST_OPTION
            )
        ).click()

    @allure.step("Нажать «Далее»")
    def click_next(self):
        self.wait.until(
            EC.element_to_be_clickable(OrderPageLocators.NEXT_BUTTON)
        ).click()

    @allure.step("Выбрать первую доступную дату")
    def select_date(self):
        self.wait.until(
            EC.element_to_be_clickable(OrderPageLocators.DATE_INPUT)
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(OrderPageLocators.DATEPICKER_DAYS)
        ).click()
        self.wait.until(
            EC.invisibility_of_element_located(
                OrderPageLocators.DATEPICKER_OVERLAY
            )
        )

    @allure.step("Выбрать первый срок аренды")
    def select_duration(self):
        dropdown = self.wait.until(
            EC.element_to_be_clickable(
                OrderPageLocators.DURATION_DROPDOWN
            )
        )
        self.scroll_into_view(dropdown)
        dropdown.click()
        self.wait.until(
            EC.element_to_be_clickable(
                OrderPageLocators.DURATION_OPTIONS
            )
        ).click()

    @allure.step("Выбрать цвет самоката")
    def select_color(self, color: str):
        locator = OrderPageLocators.COLOR_OPTIONS.get(color)
        if locator is None:
            raise ValueError(f"Неизвестный цвет самоката: {color}")

        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    @allure.step("Ввести комментарий")
    def enter_comment(self, comment: str):
        field = self.wait.until(
            EC.element_to_be_clickable(OrderPageLocators.COMMENT_INPUT)
        )
        field.send_keys(comment)

    @allure.step("Нажать «Заказать»")
    def click_submit(self):
        self.wait.until(
            EC.element_to_be_clickable(OrderPageLocators.SUBMIT_BUTTON)
        ).click()

    @allure.step("Дождаться окна подтверждения")
    def wait_for_confirm_dialog(self):
        self.wait.until(
            EC.visibility_of_element_located(
                OrderPageLocators.CONFIRM_DIALOG
            )
        )

    @allure.step("Подтвердить заказ")
    def accept_confirmation(self):
        self.wait.until(
            EC.element_to_be_clickable(
                OrderPageLocators.CONFIRM_YES_BUTTON
            )
        ).click()

        message = self.wait.until(
            EC.visibility_of_element_located(
                OrderPageLocators.SUCCESS_MESSAGE
            )
        )
        return message.text
