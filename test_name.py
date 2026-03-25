import pytest
from pydantic import BaseModel, Field, field_validator
import requests

# Модель для геолокации
class GeoModel(BaseModel):
    lat: str = Field(description="Широта", min_length=1, max_length=20)
    lng: str = Field(description="Долгота", min_length=1, max_length=20)

    @field_validator('lat', 'lng')
    @classmethod
    def validate_coordinates(cls, v: str) -> str:
        # Проверка формата координат
        try:
            float(v)
        except ValueError:
            raise ValueError(f'Координата должна быть числом: {v}')
        return v

# Модель адреса
class AddressModel(BaseModel):
    street: str = Field(description="Улица", min_length=1, max_length=100)
    suite: str = Field(description="Квартира/офис", min_length=1, max_length=50)
    city: str = Field(description="Город", min_length=1, max_length=50)
    zipcode: str = Field(description="Почтовый индекс", min_length=5, max_length=10)
    geo: GeoModel = Field(description="Географические координаты")

# Модель компании
class CompanyModel(BaseModel):
    name: str = Field(description="Название компании", min_length=1, max_length=100)
    catchPhrase: str = Field(description="Слоган", min_length=1, max_length=200)
    bs: str = Field(description="Бизнес-направление", min_length=1, max_length=100)

# Модель пользователя
class UserModel(BaseModel):
    id: int = Field(description="Идентификатор пользователя", ge=1, le=100)
    name: str = Field(description="Полное имя", min_length=3, max_length=100)
    username: str = Field(description="Имя пользователя", min_length=3, max_length=50)
    email: str = Field(description="Email адрес", min_length=5, max_length=100)
    address: AddressModel = Field(description="Адрес")
    phone: str = Field(description="Телефон", min_length=5, max_length=50)
    website: str = Field(description="Вебсайт", min_length=3, max_length=100)
    company: CompanyModel = Field(description="Компания")

# Тест валидации данных пользователя
@pytest.mark.parametrize("user_index", range(1, 11))
def test_user_validation(base_url, user_index):
    url = f"{base_url}/{user_index}"
    response = requests.get(url)

    assert response.status_code == 200, f"Ошибка запроса для пользователя {user_index}"

    user_data = response.json()
    validated_user = UserModel(**user_data)

    assert validated_user.id == user_index
    assert validated_user.name is not None
    assert validated_user.username is not None
    assert "@" in validated_user.email
    assert len(validated_user.phone) > 0
    assert len(validated_user.website) > 0
    # pytest -v