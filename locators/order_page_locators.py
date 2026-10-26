from selenium.webdriver.common.by import By


class OrderPageLocators:

    # Шаг 1 заказа
    STEP1_FORM = (By.CSS_SELECTOR, "[class*='Order_Form']")
    STEP1_INPUTS = (By.CSS_SELECTOR, "[class*='Order_Form'] input")
    STEP1_PLACEHOLDERS = {
        "* Имя": "name",
        "* Фамилия": "surname",
        "* Адрес: куда привезти заказ": "address",
        "* Станция метро": "metro",
        "* Телефон: на него позвонит курьер": "phone",
    }
    METRO_INPUT = (By.CSS_SELECTOR, 'input[placeholder="* Станция метро"]')
    METRO_OPTIONS_LIST = (By.CSS_SELECTOR, ".select-search__options")
    METRO_FIRST_OPTION = (By.CSS_SELECTOR, ".select-search__option")

    # Шаг 2 заказа
    DATE_INPUT = (By.CSS_SELECTOR, ".react-datepicker__input-container input")
    DATEPICKER_DAYS = (By.CSS_SELECTOR, ".react-datepicker__day")
    DATEPICKER_OVERLAY = (By.CSS_SELECTOR, ".react-datepicker")
    DURATION_DROPDOWN = (By.CSS_SELECTOR, ".Dropdown-control")
    DURATION_OPTIONS = (By.CSS_SELECTOR, ".Dropdown-option")
    COMMENT_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Комментарий для курьера"]')
    NEXT_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Далее')]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(@class, 'Button_Middle') and contains(normalize-space(.), 'Заказать')]")

    # Окно подтверждения
    CONFIRM_DIALOG = (By.CSS_SELECTOR, "[class*='Modal']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Да')]")
    SUCCESS_TEXT = "Заказ оформлен"

    COLOR_LABEL_TEXT = {
        "black": "чёрный жемчуг",
        "grey": "серая безысходность",
    }
