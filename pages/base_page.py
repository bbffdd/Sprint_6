import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.base_page_locators import BasePageLocators


class BasePage:
    """Базовый класс для всех Page Objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Закрыть баннер куки, если он есть")
    def dismiss_cookie(self):
        try:
            self.wait.until(EC.element_to_be_clickable(BasePageLocators.COOKIE_BUTTON)).click()
        except Exception:
            pass
