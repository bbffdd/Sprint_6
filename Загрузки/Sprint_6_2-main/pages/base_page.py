import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.base_page_locators import BasePageLocators


class BasePage:
    """Базовый класс для всех Page Objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Закрыть баннер куки, если он есть")
    def dismiss_cookie(self):
        try:
            self.wait.until(
                EC.element_to_be_clickable(BasePageLocators.COOKIE_BUTTON)
                ).click()
        except Exception:
            pass

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'})",
            element,
        )

    def click_with_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def open_url(self, url):
        self.driver.get(url)

    @property
    def window_handles(self):
        return self.driver.window_handles

    #Добавлен метод для открытия окна яндекса на подттесте клика логотипа Яндекса

    def wait_for_new_window(self, previous_handles):
        self.wait.until(EC.new_window_is_opened(previous_handles))

        for handle in self.window_handles:
            if handle not in previous_handles:
                return handle

    def switch_to_window(self, handle):
        self.driver.switch_to.window(handle)

    def get_current_url(self):
        return self.driver.current_url
