import pytest
from selenium import webdriver

from data import BASE_URL
from pages.home_page import HomePage
from pages.order_page import OrderPage


@pytest.fixture
def driver():
    browser = webdriver.Firefox()

    try:
        browser.set_page_load_timeout(30)
        browser.set_script_timeout(15)
        browser.implicitly_wait(0)
        browser.maximize_window()
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def home_page(driver):
    driver.get(BASE_URL)
    page = HomePage(driver)
    page.dismiss_cookie()
    return page


@pytest.fixture
def order_page(driver, home_page):
    return OrderPage(driver)
