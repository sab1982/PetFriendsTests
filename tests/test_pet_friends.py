from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def get_incorrected_value(value: str):
    '''функция для получения некорректного значения путем изменения первого
    символа корректного значения'''

    print("Текущее значение: " + value)
    # редактируем значение:
    # l = len(auth_key['key'])
    value = "f" + value[:-1]
    print("Новое значение: " + value)
    return value

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_api_key_incorrected_without_data(email="", password=""):
    '''тест проверяет получение api-ключа без данных'''

    status, _ = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_incorrected_without_email(email = "", password = valid_password):
    '''тест проверяет получение api-ключа
        при корректном пароле и без почты'''
    status, _ = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_incorrected_without_password(email = valid_email, password = ""):
    '''тест проверяет получение api-ключа
        при корректной почте и без пароля'''
    status, _ = pf.get_api_key(email, password)
    assert status == 403


def test_get_list_of_all_pets_incorrected_key():
    '''негативный тест на получение списка всех питомцев
        при авторизации с неверным ключем'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = get_incorrected_value(auth_key['key'])
    filter = ""

    status, results = pf.get_list_of_pets(auth_key=auth_key, filter=filter)
    assert status == 403


def test_get_list_of_my_pets_corrected():
    '''позитивный тест на получение списка только питомцев пользователя.'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    filter = "my_pets"

    status, results = pf.get_list_of_pets(auth_key=auth_key, filter=filter)
    assert status == 200
    count_pets = len(results['pets'])

    if count_pets != 0:
        print(f"my Pets = {len(results['pets'])}")
        print(results['pets'][0].keys())
        # for i in range(count_pets):
        # assert results['pets'][i]['user_id'] == auth_key['key']
    else:
        Exception("There is not pets")


def test_add_new_pet_simple_corrected():
    '''позитивный тест добавления нового питомца (упрощенный)'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    name = 'Musya'
    animal_type = 'cat'
    age = 11

    status, results = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert results['name'] == name
