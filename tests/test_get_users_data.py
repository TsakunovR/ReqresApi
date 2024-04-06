import httpx
from jsonschema import validate
from core.contracts import USER_DATA_SCHEMA
import allure

BASE_URL = 'https://reqres.in/'
LIST_USERS = 'api/users?page=2'
SINGLE_USER = 'api/users/2' #получение данных пользователя с id 2
EMAIL_ENDS = '@reqres.in'
USER_NOT_FOUND = 'api/users/23'


@allure.suite('Получение различных данных пользователей')
@allure.title('Получение списка пользователей')
def test_list_users():
    with allure.step(f'Отправляем запрос по адресу: {BASE_URL + LIST_USERS}'):
        response = httpx.get(BASE_URL + LIST_USERS)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200

    users_data = response.json()['data']
    for item in users_data:
        with allure.step(f'Проверяем структуру объекта с id: {item["id"]}'):
            validate(item, USER_DATA_SCHEMA)
            with allure.step(f'Проверяем что email оканчивается на {EMAIL_ENDS}'):
                assert item['email'].endswith(EMAIL_ENDS)
            with allure.step('Проверяем ссылку на аватар'):
                assert item['avatar'] == f'{BASE_URL}img/faces/{item["id"]}-image.jpg'


@allure.suite('Получение различных данных пользователей')
@allure.title('Получение данных одного пользователя')
def test_singel_user():
    response = httpx.get(BASE_URL + SINGLE_USER)
    assert response.status_code == 200

    users_data = response.json()['data']
    validate(users_data, USER_DATA_SCHEMA)
    assert users_data['email'].endswith(EMAIL_ENDS)
    assert users_data['avatar'] == f'{BASE_URL}img/faces/{users_data["id"]}-image.jpg'


@allure.suite('Получение различных данных пользователей')
@allure.title('Попытка получить данные по несуществующему пользователю')
def test_user_not_found():
    response = httpx.get(BASE_URL + USER_NOT_FOUND)
    assert response.status_code == 404
