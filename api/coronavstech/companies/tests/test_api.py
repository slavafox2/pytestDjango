import json
from typing import List

import logging
import pytest
from django.urls import reverse

from companies.models import Company

companies_url = reverse("companies-list")

# используете асинхронные тесты(например, с Playwright или асинхронным Django), вам может понадобиться расширенная версия:
# pytestmark = pytest.mark.django_db(transaction=True). Это позволяет тестам видеть данные, созданные в других потоках или асинхронных задачах.
pytestmark = pytest.mark.django_db


@pytest.fixture
def amazon() -> Company:
    """Компания Amazon, созданная в тестовой БД."""
    return Company.objects.create(name="Amazone")


# --------------Test Get Companies--------------

# client — это встроенная фикстура плагина pytest-django.
# Плагин pytest-django подключён у вас через pytest.ini и строку plugins: django-4.11.1 в выводе pytest.
# Этот плагин автоматически регистрирует несколько фикстур, в том числе:
# client — обёртка над django.test.Client, даёт тестовый HTTP‑клиент.
# db, django_db_* и др. — для работы с тестовой БД.
# Поэтому в pytest-стиле достаточно просто написать:
#   def test_something(client):
# и pytest сам подставит экземпляр Django-клиента, предварительно настроив Django‑окружение и
# тестовую БД (если тест помечен @pytest.mark.django_db или использует фикстуру db).


def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_exists_should_succeed(client, amazon) -> None:
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == amazon.name
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


# --------------Test Post Companies--------------


def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_existing_company_should_fail(client) -> None:
    Company.objects.create(name="apple")
    response = client.post(path=companies_url, data={"name": "apple"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]
    }


def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(path=companies_url, data={"name": "test company name"})
    assert response.status_code == 201
    response_content = response.json()
    assert response_content.get("name") == "test company name"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    response = client.post(
        path=companies_url,
        data={"name": "test company name", "status": "Layoffs"},
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("status") == "Layoffs"


def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        path=companies_url,
        data={"name": "test company name", "status": "WrongStatus"},
    )
    assert response.status_code == 400
    assert "WrongStatus" in str(response.content)
    assert "is not a valid choice" in str(response.content)


@pytest.mark.xfail
def test_should_be_ok_if_fails() -> None:
    assert 1 == 2


@pytest.mark.skip
def test_should_be_skipped() -> None:
    assert 1 == 2


def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")


def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)


logger = logging.getLogger("CORONA_LOGS")


def function_that_logs_something() -> None:
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")


## -> запуск тест коммандой pytest -v -s -k "logged"
##
# Куда “вставляется” logged в pytest -v -s -k "logged"
# logged попадает в опцию -k и используется как строковый фильтр по именам.
# Что фильтруется: имена тестов и “узлы” коллекции pytest (имя файла, имя класса, имя функции, иногда часть nodeid вроде test_api.py::Test...::test_logged...).
# Как работает: pytest оставляет к запуску только те тесты, у которых где-то в имени встречается logged.
# В вашем случае тест называется test_logged_warning_level, поэтому -k "logged" его выбирает.
# Примеры:
# pytest -k "logged" → запустит всё, где есть logged
# pytest -k "logged and warning" → где есть и logged, и warning
# pytest -k "logged and not error" → где есть logged, но нет error


def test_logged_warning_level(caplog) -> None:
    caplog.set_level(logging.WARNING, logger="CORONA_LOGS")
    function_that_logs_something()
    assert "I am logging CoronaVirus Exception" in caplog.text


def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logger.info("I am logging info level")
        assert "I am logging info level" in caplog.text


# --------------Learn about fixtures tests--------------

# @pytest.fixture
# def companies(request, company)-> List[Company]:
#     companies = []
#     names = request.param
#     for name in names:
#         companies.append(company(name=name))
#     return companies
        

# @pytest.fixture()
# def company(**kwargs):
#     def _company_factory(**kwargs) -> Company:
#         company_name = kwargs.pop("name", "Test Company INC")
#         return Company.objects.create(name=company_name, **kwargs)

#     return _company_factory


# def test_multiple_companies_exists_should_succeed(client, company) -> None:
#     tiktok: Company = company(name="Tiktok")
#     twitch: Company = company(name="Twitch")
#     test_company: Company = company()
#     company_names = {tiktok.name, twitch.name, test_company.name}
#     response_companies = client.get(companies_url).json()
#     assert len(company_names) == len(response_companies)
#     response_company_names = set(
#         map(lambda company: company.get("name"), response_companies)
#     )
#     assert company_names == response_company_names

# pytest style
@pytest.mark.parametrize(
    "companies",
    [["Tiktok", "Twitch", "Test Company INC"], ["Facebook", "Instagram"]],
    ids=["3 T companies", "Zuckerberg's companies"],
    indirect=True,
)
def test_multiple_companies_exists_should_succeed(client, companies) -> None:    
    # строка через генератор множества:
    company_names = {x.name for x in companies} # company_names = set(map(lambda x: x.name, companies))
    print(company_names)
    response_companies = client.get(companies_url).json()
    assert len(company_names) == len(response_companies)
    response_company_names = set(
        map(lambda company: company.get("name"), response_companies)
    )
    assert company_names == response_company_names
