from selenium.webdriver.common.by import By


class OrderPageLocators:
    NEXT_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(.), 'Далее')]",
    )

    # Шаг 1 заказа
    STEP1_FIELDS = {
        "name": (
            By.CSS_SELECTOR,
            'input[placeholder="* Имя"]',
        ),
        "surname": (
            By.CSS_SELECTOR,
            'input[placeholder="* Фамилия"]',
        ),
        "address": (
            By.CSS_SELECTOR,
            'input[placeholder="* Адрес: куда привезти заказ"]',
        ),
        "phone": (
            By.CSS_SELECTOR,
            'input[placeholder="* Телефон: на него позвонит курьер"]',
        ),
    }

    STEP_1_METRO_INPUT = (
        By.CSS_SELECTOR,
        'input[placeholder="* Станция метро"]',
    )
    STEP_1_METRO_OPTIONS_LIST = (
        By.CSS_SELECTOR,
        ".select-search__options",
    )
    STEP_1_METRO_OPTIONS = (
        By.CSS_SELECTOR,
        ".select-search__option",
    )

    # Шаг 2 заказа
    STEP_2_DATE_INPUT = (
        By.CSS_SELECTOR,
        ".react-datepicker__input-container input",
    )
    STEP_2_DATEPICKER_DAYS = (
        By.CSS_SELECTOR,
        ".react-datepicker__day:not(.react-datepicker__day--disabled):"
        "not(.react-datepicker__day--outside-month)",
    )
    STEP_2_DATEPICKER_OVERLAY = (
        By.CSS_SELECTOR,
        ".react-datepicker",
    )
    STEP_2_DURATION_DROPDOWN = (
        By.CSS_SELECTOR,
        ".Dropdown-control",
    )
    STEP_2_DURATION_OPTIONS = (
        By.CSS_SELECTOR,
        ".Dropdown-option",
    )
    STEP_2_COMMENT_INPUT = (
        By.CSS_SELECTOR,
        'input[placeholder="Комментарий для курьера"]',
    )
    STEP_2_SUBMIT_BUTTON = (
        By.XPATH,
        "//button[contains(@class, 'Button_Middle') "
        "and contains(normalize-space(.), 'Заказать')]",
    )
    STEP_2_COLOR_OPTIONS = {
        "black": (
            By.XPATH,
            "//label[contains(normalize-space(.), 'чёрный жемчуг')]",
        ),
        "grey": (
            By.XPATH,
            "//label[contains(normalize-space(.), 'серая безысходность')]",
        ),
    }

    # Шаг 3 — окно подтверждения
    STEP_3_CONFIRM_DIALOG = (
        By.CSS_SELECTOR,
        "[class*='Modal']",
    )
    STEP_3_CONFIRM_YES_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(.), 'Да')]",
    )
    STEP_3_SUCCESS_MESSAGE = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Заказ оформлен')]",
    )
    STEP_3_SUCCESS_TEXT = "Заказ оформлен"
