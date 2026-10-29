import allure

from locators.home_page_locators import HomePageLocators
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object главной страницы."""

    @allure.step("Открыть FAQ #{index} и проверить, что он раскрыт")
    def open_faq_and_check(self, index: int) -> bool:
        self._click_index(HomePageLocators.FAQ_BUTTONS, index)
        return self._wait_for_visible_index(
            HomePageLocators.FAQ_PANELS,
            index,
        )

    @allure.step("Нажать кнопку заказа: {entry_point}")
    def click_order_button(self, entry_point: str) -> None:
        buttons = {
            "header": HomePageLocators.HEADER_ORDER_BUTTON,
            "bottom": HomePageLocators.BOTTOM_ORDER_BUTTON,
        }

        locator = buttons.get(entry_point)
        if locator is None:
            raise ValueError("entry_point должен быть 'header' или 'bottom'")

        self._click(locator)

    @allure.step("Перейти по логотипу Самоката")
    def click_scooter_logo(self) -> str:
        self._click(HomePageLocators.SCOOTER_LOGO)
        self._wait_for_url_contains(HomePageLocators.SCOOTER_HOME_URL)
        return self._get_current_url()

    @allure.step("Открыть логотип Яндекса в новом окне")
    def click_yandex_logo(self) -> str:
        return self._click_and_get_new_window_url(
            HomePageLocators.YANDEX_LOGO
        )

    @allure.step("Получить alt изображения логотипа Яндекса")
    def get_yandex_logo_alt(self) -> str:
        return self._get_attribute(
            HomePageLocators.YANDEX_LOGO_IMAGE,
            "alt",
        )
