# Sprint 6 — UI-тестирование с Selenium + POM

Тесты расположены в `tests/`
Сгруппированы в 2 категории:
1. TestFAQ — каждый вопрос FAQ — отдельный метод
2. TestOrder — позитивный сценарий заказа самоката

В сценарии позитивного заказа не учитываются негативные ветки заполнения и поведения приложения.

Структура:
- `pages/` — page objects
- `locators/` — локаторы
- `tests/` — тесты
- `data.py` — тестовые данные

Общие элементы (взаимодействие с cookie-баннером) вынесены в `pages/base_page.py` и `locators/base_page_locators.py`.

Allure-отчёт генерируется в `allure_results/`, собирается в `allure_report/` и коммитится в репозиторий.
Для запуска и генерации отчёта:

```bash
pytest tests/test_scooter.py --alluredir=allure_results
allure generate allure_results -o allure_report --clean
git add allure_report/ && git commit -m "update allure report"
```

