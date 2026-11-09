import allure
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.home_page_locators import HomePageLocators


class HomePage(BasePage):
    """PO для главной страницы."""

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Открыть FAQ #{index} и проверить ответ")
    def open_faq_and_check(self, index: int):
        buttons_locator = HomePageLocators.FAQ_BUTTONS
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(buttons_locator)
        )

        button = buttons[index]
        self.scroll_into_view(button)
        self.wait.until(EC.element_to_be_clickable(button))
        try:
            button.click()
        except Exception:
            self.click_with_js(button)

        panels = self.wait.until(
            EC.presence_of_all_elements_located(HomePageLocators.FAQ_PANELS)
        )
        panel = panels[index]

        self.wait.until(EC.visibility_of(panel))
        return panel.is_displayed()

    @allure.step("Нажать кнопку заказа: {entry_point}")
    def click_order_button(self, entry_point: str):
        buttons = {
            "header": HomePageLocators.HEADER_ORDER_BUTTON,
            "bottom": HomePageLocators.BOTTOM_ORDER_BUTTON,
        }

        locator = buttons.get(entry_point)
        if locator is None:
            raise ValueError(
                "entry_point должен быть 'header' или 'bottom'"
            )

        button = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        self.scroll_into_view(button)
        button.click()

    @allure.step("Нажать на логотип Самоката и получить ссылку")
    def click_scooter_logo(self):
        logo = self.wait.until(
            EC.element_to_be_clickable(HomePageLocators.SCOOTER_LOGO)
        )
        href = logo.get_attribute("href")
        logo.click()
        return href

    @allure.step("Нажать на логотип Яндекса и получить URL нового окна")
    def click_yandex_logo(self):
        old_handles = self.window_handles

        logo = self.wait.until(
            EC.element_to_be_clickable(HomePageLocators.YANDEX_LOGO)
        )
        logo.click()

        new_handle = self.wait_for_new_window(old_handles)
        self.switch_to_window(new_handle)
        self.wait.until(EC.url_contains("ya.ru"))
        return self.get_current_url()

    @allure.step("Получить alt изображения логотипа Яндекса")
    def get_yandex_logo_alt(self):
        image = self.wait.until(
            EC.visibility_of_element_located(
                HomePageLocators.YANDEX_LOGO_IMAGE
            )
        )
        return image.get_attribute("alt")