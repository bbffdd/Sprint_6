from selenium.webdriver.common.by import By


class HomePageLocators:

    FAQ_BUTTONS = (By.CSS_SELECTOR, ".accordion__button")
    FAQ_PANELS = (By.CSS_SELECTOR, ".accordion__panel")
    SCOOTER_LOGO = (By.CSS_SELECTOR, "a[class*='LogoScooter']")
    YANDEX_LOGO = (By.CSS_SELECTOR, "a[class*='LogoYandex']")
    SCOOTER_HOME_URL = "https://qa-scooter.education-services.ru/"
    YANDEX_LOGO_IMAGE = (By.CSS_SELECTOR,"a[class*='LogoYandex'] img",)

    # Локаторы кнопок заказа.
    HEADER_ORDER_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'Header_Nav')]"
        "//button[contains(normalize-space(.), 'Заказать')]",
    )
    BOTTOM_ORDER_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'Home_FinishButton')]"
        "//button[contains(normalize-space(.), 'Заказать')]",
    )