import glob
import os

import pytest
from selenium import webdriver

from pages.home_page import HomePage

@pytest.fixture
def home_page():
    import os, glob
    os.environ.setdefault("WAYLAND_DISPLAY", "wayland-0")
    from selenium.webdriver.firefox.options import Options
    options = Options()
    snaps = glob.glob("/snap/firefox/*/usr/lib/firefox/firefox")
    if snaps:
        options.binary_location = sorted(snaps)[-1]
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(15)
    driver.implicitly_wait(0)
    driver.get("https://qa-scooter.education-services.ru/")
    HomePage(driver).dismiss_cookie()
    yield HomePage(driver)
    driver.quit()


@pytest.fixture
def wait(home_page):
    """Короткий wait для явных ожиданий."""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec
    return WebDriverWait(home_page.driver, 10)
