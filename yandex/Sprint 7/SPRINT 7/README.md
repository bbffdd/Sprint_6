# Sprint 7 Final Project — API Tests for Scooter Courier

## Structure
```
SPRINT 7/
├── conftest.py                # fixtures + helpers (generate_random_string, register_courier)
├── test_courier_create.py     # tests for POST /courier
├── test_courier_login.py      # tests for POST /courier/login
├── test_create_order.py       # tests for POST /order (parametrized)
├── test_order_list.py         # tests for GET /orders
├── pytest.ini
└── README.md
```

## Run
```bash
cd "/home/hamb/Загрузки/SPRINT 7"
pytest -v
pytest -v --alluredir=allure-results
allure serve allure-results
```

## Test Results (verified)
- **15 passed** — all tests green against live API
- Allure report generated in `allure-results/`

## API Base
`https://qa-scooter.education-services.ru/api/v1`

## Endpoints used
| Handset | Method | Path |
|---|---|---|
| Create courier | POST | `/courier` |
| Courier login | POST | `/courier/login` |
| Create order | POST | `/orders` |
| Order list | GET | `/orders` |

## Techniques from Sprint 7 materials applied
- **Сериализация**: `json.dumps(payload)` + `Content-Type: application/json` header (as taught in "Сериализация" lesson)
- **Десериализация**: `response.json()` to parse JSON responses (as taught in "Десериализация" lesson)
- **Параметризация**: `@pytest.mark.parametrize` for BLACK/GREY color tests (as taught in "Как хранить данные")
- **Изоляция**: pytest fixtures in `conftest.py` — each test prepares its own data (as taught in "Изоляция в тестах")
- **Positive/negative testing**: happy-path + error cases for each endpoint
