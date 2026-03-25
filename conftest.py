import pytest

@pytest.fixture
def base_url():
    # Фикстура для основного эндпоинта
    return "https://jsonplaceholder.typicode.com/users"