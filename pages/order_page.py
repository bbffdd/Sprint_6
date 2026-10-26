import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.order_page_locators import OrderPageLocators


class OrderPage(BasePage, OrderPageLocators):
    """PO для страницы-формы заказа самоката."""

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.loc = OrderPageLocators()

    # ----- Шаги -----

    @allure.step('Заполнить форму заказа')
    def order_step(self, data: dict):
        self.fill_step1(data)
        self.click_next()
        self.fill_step2(data)
        self.click_submit()

    @allure.step('Заполнить этап 1, пользовательские данные')
    def fill_step1(self, data: dict):
        self.wait.until(EC.visibility_of_element_located(self.STEP1_FORM))
        self.wait.until(EC.presence_of_all_elements_located(self.STEP1_INPUTS))
        inputs = self.driver.find_elements(*self.STEP1_INPUTS)
        for inp in inputs:
            ph = inp.get_attribute("placeholder")
            key = self.STEP1_PLACEHOLDERS.get(ph)
            if key and key in data:
                inp.send_keys(data[key])

        self.wait.until(EC.element_to_be_clickable(self.METRO_INPUT)).click()
        self.wait.until(EC.visibility_of_element_located(self.METRO_OPTIONS_LIST))
        self.wait.until(EC.element_to_be_clickable(self.METRO_FIRST_OPTION)).click()

    @allure.step('Клик Далее ')
    def click_next(self):
        self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()
        return self

    @allure.step('Заполнить этап 2, параметры аренды')
    def fill_step2(self, data: dict):
        date_inp = self.wait.until(EC.element_to_be_clickable(self.DATE_INPUT))
        date_inp.click()
        self.wait.until(EC.element_to_be_clickable(self.DATEPICKER_DAYS)).click()
        try:
            self.wait.until(EC.invisibility_of_element_located(self.DATEPICKER_OVERLAY))
        except Exception:
            pass

        dropdown = self.wait.until(EC.element_to_be_clickable(self.DURATION_DROPDOWN))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)
        dropdown.click()
        self.wait.until(EC.element_to_be_clickable(self.DURATION_OPTIONS)).click()

        if data.get("color"):
            label_text = self.COLOR_LABEL_TEXT.get(data["color"])
            if label_text:
                label = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//label[contains(normalize-space(.), '{label_text}')]"))
                )
                label.click()

        comment = self.wait.until(EC.element_to_be_clickable(self.COMMENT_INPUT))
        comment.send_keys(data.get("comment", ""))

    @allure.step('Подтвердить заказ отправки заполненных форм заказа')
    def click_submit(self):
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON)).click()

    # ----- Диалоги -----

    @allure.step('Убедиться, что пришло окно подтверждения регистрации заказа')
    def wait_for_confirm_dialog(self):
        self.wait.until(EC.visibility_of_element_located(self.CONFIRM_DIALOG))
        return self.driver.find_element(*self.CONFIRM_DIALOG)

    @allure.step('Подтвердить заказ')
    def accept_confirmation(self):
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_YES_BUTTON)).click()
        success_xpath = f"//*[contains(normalize-space(.), '{OrderPage.SUCCESS_TEXT}')]"
        self.wait.until(EC.visibility_of_element_located((By.XPATH, success_xpath)))
        return self.driver.find_element(*self.CONFIRM_DIALOG).text
