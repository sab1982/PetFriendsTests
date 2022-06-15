from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def get_incorrected_value(value: str):
    '''функция для получения некорректного значения путем изменения первого
    символа корректного значения'''

    print("Текущее значение: " + value)

    value = "f" + value[:-1]
    print("Новое значение: " + value)
    return value


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''тест проверяет получение api-ключа при корректных
    данных почты и пароля'''

    status, results = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in results


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, results = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(results['pets']) > 0


def test_get_api_key_without_data(email="", password=""):
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
    """позитивный тест на получение списка только питомцев пользователя."""

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
    '''позитивный тест добавления нового питомца (простой)'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    name = 'Pasha'
    animal_type = 'budgie'
    age = 1

    status, results = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert results['name'] == name


def test_add_new_pet():
    '''позитивный тест добавления нового питомца (с фото)'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    name = 'Musya'
    animal_type = 'cat'
    age = '11'
    pet_photo = 'images/Musya.jpg'
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, results = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert results['name'] == name
    print(type(results))
    print(results)


def test_successful_delete_self_pet():
    """Проверка возможности удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Tishka', animal_type='SuperCat', age=15):
    """Проверка возможности обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, results = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert results['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
