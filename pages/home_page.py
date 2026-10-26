import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.home_page_locators import HomePageLocators
from locators.order_page_locators import OrderPageLocators

import data as app_data


class HomePage(BasePage, HomePageLocators):
    """PO для Главной страницы"""

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    # ----- Шаги -----

    @allure.step('Открыть FAQ  #{index}')
    def open_faq_and_check(self, index: int):
        from selenium.webdriver.support.ui import WebDriverWait as _WW
        from selenium.webdriver.support import expected_conditions as EC
        self.wait.until(EC.presence_of_all_elements_located(self.FAQ_BUTTONS))
        buttons = self.driver.find_elements(*self.FAQ_BUTTONS)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", buttons[index])
        # ждём, пока кнопка с нужным индексом станет кликабельной, затем кликаем напрямую
        _WW(self.driver, 10).until(
            lambda d: d.find_elements(*self.FAQ_BUTTONS)[index].is_displayed()
            and d.find_elements(*self.FAQ_BUTTONS)[index].is_enabled()
        )
        try:
            buttons[index].click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", buttons[index])
        panels = self.driver.find_elements(*self.FAQ_PANELS)
        return panels[index].get_attribute("hidden") is None

    @allure.step('Click order button ({entry_point})')
    def click_order_button(self, entry_point: str):
        self.wait.until(EC.presence_of_all_elements_located(self.ORDER_BUTTONS))
        buttons = self.driver.find_elements(*self.ORDER_BUTTONS)
        btn = buttons[0] if entry_point == "header" else buttons[3]
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",
                                     buttons[0] if entry_point == "header" else buttons[3])
        buttons[0 if entry_point == "header" else 3].click()
        from pages.order_page import OrderPage
        return OrderPage(self.driver)

    @allure.step('Заполнить Шаг, подтвердить заказ')
    def order_scooter(self, data: dict):
        for entry_point in ("header", "bottom"):
            order_page = self.click_order_button(entry_point)
            order_page.order_step(data)
            order_page.wait_for_confirm_dialog()
            order_page.accept_confirmation()
            self.driver.get(app_data.BASE_URL)
            self.wait.until(EC.invisibility_of_element_located(OrderPageLocators.CONFIRM_DIALOG))


    @allure.step('Перейти по лого Самоката и нужный атрибут')
    def click_scooter_logo(self):
        logo = self.wait.until(EC.element_to_be_clickable(self.SCOOTER_LOGO))
        href = logo.get_attribute("href")
        logo.click()
        return href

    @allure.step('Кликнуть лого яндекса и вернуть новое окно.')
    def click_yandex_logo(self):
        old_handles = self.driver.window_handles
        logo = self.wait.until(EC.element_to_be_clickable(self.YANDEX_LOGO))
        logo.click()
        self.wait.until(EC.new_window_is_opened(old_handles))
        return [h for h in self.driver.window_handles if h not in old_handles][0]
