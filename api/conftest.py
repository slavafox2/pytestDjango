import pytest

from api.coronavstech.companies.models import Company
# from companies.models import Company

@pytest.fixture
def amazon() -> Company:
    """Компания Amazon, созданная в тестовой БД."""
    return Company.objects.create(name="Amazone")
