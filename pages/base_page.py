import allure
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.base_page_locators import BasePageLocators

class BasePage:
    """Общие Selenium-операции для Page Objects."""

    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def _find_all(self, locator):
        return self._driver.find_elements(*locator)

    def _scroll_into_view(self, element):
        self._driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )

    def _click(self, locator):
        element = self._wait.until(
            EC.element_to_be_clickable(locator)
        )
        self._scroll_into_view(element)
        element.click()

    def _click_index(self, locator, index):
        if index < 0:
            raise IndexError(f"Индекс не может быть отрицательным: {index}")

        def find_clickable_element(driver):
            elements = driver.find_elements(*locator)

            if index >= len(elements):
                return False

            element = elements[index]
            if element.is_displayed() and element.is_enabled():
                return element

            return False

        element = self._wait.until(find_clickable_element)
        self._scroll_into_view(element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self._driver.execute_script("arguments[0].click();", element)

    def _click_text(self, locator, text):
        expected_text = text.strip()

        def find_matching_element(driver):
            for element in driver.find_elements(*locator):
                if (
                    element.is_displayed()
                    and element.is_enabled()
                    and element.text.strip() == expected_text
                ):
                    return element

            return False

        element = self._wait.until(find_matching_element)
        self._scroll_into_view(element)
        element.click()

    def _type(self, locator, value):
        element = self._wait.until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(value)

    def _wait_visible(self, locator):
        return self._wait.until(
            EC.visibility_of_element_located(locator)
        )

    def _wait_invisible(self, locator):
        return self._wait.until(
            EC.invisibility_of_element_located(locator)
        )

    def _get_text_at_index(self, locator, index):
        elements = self._find_all(locator)

        if index < 0 or index >= len(elements):
            raise IndexError(f"Нет элемента с индексом {index}")

        return elements[index].text.strip()

    def get_text(self, locator):
        """Возвращает текст видимого элемента."""
        element = self._wait.until(
            EC.visibility_of_element_located(locator)
        )
        return element.text.strip()

    def _wait_for_visible_index(self, locator, index):
        if index < 0:
            raise IndexError(f"Индекс не может быть отрицательным: {index}")

        def is_visible(driver):
            elements = driver.find_elements(*locator)
            return (
                index < len(elements)
                and elements[index].is_displayed()
                and elements[index].get_attribute("hidden") is None
            )

        return self._wait.until(is_visible)

    def _get_attribute(self, locator, attribute):
        element = self._wait.until(
            EC.visibility_of_element_located(locator)
        )
        return element.get_attribute(attribute)

    def _wait_for_url_contains(self, value):
        return self._wait.until(EC.url_contains(value))

    def _get_current_url(self):
        return self._driver.current_url

    def _click_and_get_new_window_url(self, locator):
        original_handle = self._driver.current_window_handle
        handles_before = set(self._driver.window_handles)

        self._click(locator)
        self._wait.until(EC.new_window_is_opened(handles_before))

        new_handles = set(self._driver.window_handles) - handles_before
        if not new_handles:
            raise AssertionError("После клика новое окно не открылось")

        new_handle = new_handles.pop()

        try:
            self._driver.switch_to.window(new_handle)
            self._wait.until(
                lambda driver: (
                    driver.current_url
                    and driver.current_url != "about:blank"
                )
            )
            return self._get_current_url()
        finally:
            if new_handle in self._driver.window_handles:
                self._driver.close()

            if original_handle in self._driver.window_handles:
                self._driver.switch_to.window(original_handle)

    @allure.step("Закрыть баннер cookie, если он отображается")
    def dismiss_cookie(self) -> None:
        try:
            self._click(BasePageLocators.COOKIE_BUTTON)
        except TimeoutException:
            pass
