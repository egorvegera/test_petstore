import pytest
import requests
import allure

BASE_URL = "https://petstore.swagger.io/v2"

@pytest.fixture
def api_client():
    return requests

# Фикстура для создания питомца
@pytest.fixture
def create_pet(api_client):
    payload = {
        "id": 12345,
        "name": "TestDog",
        "status": "available"
    }
    api_client.post(f"{BASE_URL}/pet", json=payload)
    return 12345

# Фикстура для создания пользователя
@pytest.fixture
def create_user(api_client):
    payload = {
        "id": 54321,
        "username": "testuser",
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "password": "123456",
        "phone": "123-456-7890"
    }
    api_client.post(f"{BASE_URL}/user", json=payload)
    return "testuser"

# Фикстура для создания заказа
@pytest.fixture
def create_order(api_client):
    payload = {
        "id": 98765,
        "petId": 12345,
        "quantity": 1,
        "shipDate": "2025-04-08T10:00:00Z",
        "status": "placed",
        "complete": False
    }
    api_client.post(f"{BASE_URL}/store/order", json=payload)
    return 98765

# Pet tests
@allure.feature("Pet")
@allure.title("Создание нового питомца")
@allure.description("Проверяет успешное создание питомца через POST /pet")
def test_create_pet(api_client):
    payload = {"id": 12345, "name": "TestDog", "status": "available"}
    response = api_client.post(f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "TestDog"

@allure.feature("Pet")
@allure.title("Получение питомца по ID")
@allure.description("Проверяет получение данных питомца по ID через GET /pet/{petId}")
def test_get_pet_by_id(api_client, create_pet):
    response = api_client.get(f"{BASE_URL}/pet/{create_pet}")
    assert response.status_code == 200
    assert response.json()["id"] == 12345

@allure.feature("Pet")
@allure.title("Обновление данных питомца")
@allure.description("Проверяет обновление имени и статуса питомца через PUT /pet")
def test_update_pet(api_client):
    payload = {"id": 12345, "name": "UpdatedDog", "status": "sold"}
    response = api_client.put(f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedDog"

@allure.feature("Pet")
@allure.title("Удаление питомца")
@allure.description("Проверяет удаление питомца по ID через DELETE /pet/{petId}")
def test_delete_pet(api_client, create_pet):
    response = api_client.delete(f"{BASE_URL}/pet/{create_pet}")
    assert response.status_code == 200

@allure.feature("Pet")
@allure.title("Запрос несуществующего питомца")
@allure.description("Проверяет обработку запроса несуществующего питомца через GET /pet/{petId}")
def test_get_nonexistent_pet(api_client):
    response = api_client.get(f"{BASE_URL}/pet/99999")
    assert response.status_code == 404

# User tests
@allure.feature("User")
@allure.title("Создание нового пользователя")
@allure.description("Проверяет успешное создание пользователя через POST /user")
def test_create_user(api_client):
    payload = {"id": 54321, "username": "testuser", "firstName": "Test", "lastName": "User", "email": "test@example.com", "password": "123456", "phone": "123-456-7890"}
    response = api_client.post(f"{BASE_URL}/user", json=payload)
    assert response.status_code == 200

@allure.feature("User")
@allure.title("Получение пользователя по имени")
@allure.description("Проверяет получение данных пользователя по username через GET /user/{username}")
def test_get_user_by_username(api_client, create_user):
    response = api_client.get(f"{BASE_URL}/user/{create_user}")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@allure.feature("User")
@allure.title("Обновление данных пользователя")
@allure.description("Проверяет обновление данных пользователя через PUT /user/{username}")
def test_update_user(api_client):
    payload = {"id": 54321, "username": "testuser", "firstName": "Updated", "lastName": "User", "email": "updated@example.com", "password": "654321", "phone": "098-765-4321"}
    response = api_client.put(f"{BASE_URL}/user/testuser", json=payload)
    assert response.status_code == 200

@allure.feature("User")
@allure.title("Удаление пользователя")
@allure.description("Проверяет удаление пользователя по username через DELETE /user/{username}")
def test_delete_user(api_client):
    response = api_client.delete(f"{BASE_URL}/user/testuser")
    assert response.status_code == 200

@allure.feature("User")
@allure.title("Вход пользователя в систему")
@allure.description("Проверяет вход пользователя через GET /user/login с параметрами username и password")
def test_login_user(api_client):
    response = api_client.get(f"{BASE_URL}/user/login", params={"username": "testuser", "password": "654321"})
    assert response.status_code == 200
    assert "logged in user session" in response.text

# Store tests
@allure.feature("Store")
@allure.title("Создание нового заказа")
@allure.description("Проверяет успешное создание заказа через POST /store/order")
def test_create_order(api_client):
    payload = {"id": 98765, "petId": 12345, "quantity": 1, "shipDate": "2025-04-08T10:00:00Z", "status": "placed", "complete": False}
    response = api_client.post(f"{BASE_URL}/store/order", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == 98765

@allure.feature("Store")
@allure.title("Получение заказа по ID")
@allure.description("Проверяет получение данных заказа по ID через GET /store/order/{orderId}")
def test_get_order_by_id(api_client, create_order):
    response = api_client.get(f"{BASE_URL}/store/order/{create_order}")
    assert response.status_code == 200
    assert response.json()["petId"] == 12345

@allure.feature("Store")
@allure.title("Удаление заказа")
@allure.description("Проверяет удаление заказа по ID через DELETE /store/order/{orderId}")
def test_delete_order(api_client):
    response = api_client.delete(f"{BASE_URL}/store/order/98765")
    assert response.status_code == 200

@allure.feature("Store")
@allure.title("Получение инвентаря магазина")
@allure.description("Проверяет получение текущего инвентаря через GET /store/inventory")
def test_get_inventory(api_client):
    response = api_client.get(f"{BASE_URL}/store/inventory")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

@allure.feature("Store")
@allure.title("Запрос несуществующего заказа")
@allure.description("Проверяет обработку запроса несуществующего заказа через GET /store/order/{orderId}")
def test_get_nonexistent_order(api_client):
    response = api_client.get(f"{BASE_URL}/store/order/99999")
    assert response.status_code == 404
