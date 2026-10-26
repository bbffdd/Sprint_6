from selenium.webdriver.common.by import By


class HomePageLocators:

    ORDER_BUTTONS = (By.CSS_SELECTOR, "button")
    FAQ_BUTTONS = (By.CSS_SELECTOR, ".accordion__button")
    FAQ_PANELS = (By.CSS_SELECTOR, ".accordion__panel")
    SCOOTER_LOGO = (By.CSS_SELECTOR, "a[class*='LogoScooter']")
    YANDEX_LOGO = (By.CSS_SELECTOR, "a[class*='LogoYandex']")
    SCOOTER_HOME_URL = "https://qa-scooter.education-services.ru/"
