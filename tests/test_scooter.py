import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from locators.home_page_locators import HomePageLocators
import data as app_data


@allure.feature("FAQ")
class TestFAQ:
    """Тесты «Часто задаваемых вопросов». Параметризован по индексу."""

    @pytest.mark.parametrize("idx", app_data.FAQ_INDICES, ids=[f"q{i}" for i in app_data.FAQ_INDICES])
    @allure.story("Раскрытие вопроса FAQ")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Проверяет, что вопрос FAQ с индексом {idx} раскрывается по клику.")
    def test_faq_question_opens(self, home_page: HomePage, idx: int):
        assert home_page.open_faq_and_check(idx), f"FAQ-вопрос {idx} не раскрыт"


@allure.feature("Заказ самоката")
class TestOrder:
    """Тесты позитивного сценария заказа самоката."""

    @pytest.mark.parametrize("data", app_data.ORDER_DATA, ids=["ivanov", "petrova", "sidorov"])
    @allure.story("Позитивный сценарий заказа")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Заполняется форма заказа с разными данными, проверяется появление модалки подтверждения.")
    def test_order_success(self, home_page: HomePage, data: dict):
        home_page.order_scooter(data)

    @allure.story("Навигация по логотипам")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Если нажать на логотип «Самоката», попадёшь на главную страницу «Самоката».")
    def test_scooter_logo_navigates_home(self, home_page: HomePage):
        href = home_page.click_scooter_logo()
        assert href and HomePageLocators.SCOOTER_HOME_URL in href, f"Логотип ведёт не на главную: {href}"
        assert HomePageLocators.SCOOTER_HOME_URL in home_page.driver.current_url, (
            f"После клика URL: {home_page.driver.current_url}"
        )

    @allure.story("Навигация по логотипам")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Если нажать на логотип Яндекса, в новом окне через редирект откроется главная страница Яндекса.")
    def test_yandex_logo_opens_new_window(self, home_page: HomePage):
        new_handle = home_page.click_yandex_logo()
        home_page.driver.switch_to.window(new_handle)
        home_page.wait.until(EC.url_contains("ya.ru"))
        assert home_page.driver.current_url.startswith("https://ya.ru"), (
            f"Новая вкладка не ведёт на Яндекс. URL: {home_page.driver.current_url}"
        )
        home_page.driver.switch_to.window(home_page.driver.window_handles[0])

    @allure.story("Навигация по логотипам")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Проверяет alt-атрибут изображения внутри логотипа Яндекса.")
    def test_yandex_logo_text(self, home_page: HomePage):
        """Проверяем, что логотип Яндекса содержит alt='Yandex'."""
        logo = home_page.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "a[class*='LogoYandex']")
        ))
        # лямбда: условие зависит от драйвера, проверяем alt у вложенного img
        home_page.wait.until(lambda _: logo.find_element(By.TAG_NAME, "img").get_attribute("alt") == "Yandex")
