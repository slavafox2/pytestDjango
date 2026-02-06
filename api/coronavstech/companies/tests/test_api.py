import json
import logging
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse

from companies.models import Company


@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self):
        pass


# --------------Test GET Companies--------------
class TestGetCompanies(BasicCompanyAPITestCase):

    def test_zero_companies_should_return_empty_list(self) -> None:

        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self) -> None:

        amazon = Company.objects.create(name="Amazone")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        print(response_content)
        assert response.status_code == 200
        assert response_content.get("name") == amazon.name
        assert response_content.get("status") == "Hiring"
        assert response_content.get("application_link") == ""
        assert response_content.get("notes") == ""

        amazon.delete()


# --------------Test Post Companies--------------
class TestPostCompanies(BasicCompanyAPITestCase):

    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    def test_create_existing_company_should_fail(self) -> None:
        # сначала создаём компанию в БД
        Company.objects.create(name="amazon")

        # затем пробуем создать компанию с тем же именем через API
        response = self.client.post(path=self.companies_url, data={"name": "amazon"})
        assert response.status_code == 400
        assert json.loads(response.content) == {
            "name": ["company with this name already exists."]
        }

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "test company name"}
        )
        assert response.status_code == 201
        response_content = response.json()
        assert response_content.get("name") == "test company name"
        assert response_content.get("status") == "Hiring"
        assert response_content.get("application_link") == ""
        assert response_content.get("notes") == ""

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        response = self.client.post(
            path=self.companies_url,
            data={"name": "test company name", "status": "Layoffs"},
        )
        assert response.status_code == 201
        response_content = json.loads(response.content)
        assert response_content.get("status") == "Layoffs"

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(
            path=self.companies_url,
            data={"name": "test company name", "status": "WrongStatus"},
        )
        assert response.status_code == 400
        assert "WrongStatus" in str(response.content)
        assert "is not a valid choice" in str(response.content)

    @pytest.mark.xfail
    def test_should_be_ok_if_fails(self) -> None:
        assert 1 == 2

    @pytest.mark.skip
    def test_should_be_ok_if_fails(self) -> None:
        assert 1 == 2

    def raise_covid19_exception(self) -> None:
        raise ValueError("CoronaVirus Exception")

    def test_raise_covid19_exception_should_pass(self) -> None:
        with pytest.raises(ValueError) as e:
            self.raise_covid19_exception()
        assert "CoronaVirus Exception" == str(e.value)

    #
    # logger = logging.getLogger("CORONA_LOGS")
    #
    # def function_that_logs_something(self) -> None:
    #     try:
    #         raise ValueError("CoronaVirus Exception")
    #     except ValueError as e:
    #         self.logger.warning(f"I am logging {str(e)}")
    #
    # def test_logged_warning_level(self) -> None:
    #     with self.assertLogs("CORONA_LOGS", level="WARNING") as captured:
    #         self.function_that_logs_something()
    #
    #     assert any(
    #         "I am logging CoronaVirus Exception" in message
    #         for message in captured.output
    #     )
    #
