import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)

        status = res.status_code
        results = ""
        try:
            results = res.json()
        except json.decoder.JSONDecodeError:
            results = res.text

        return status, results

    def get_list_of_pets(self, auth_key, filter):

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)

        status = res.status_code
        results = ""
        try:
            results = res.json()
        except json.decoder.JSONDecodeError:
            results = res.text

        return status, results

    def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str, age):

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        status = res.status_code

        results = ""
        try:
            results = res.json()
        except json.decoder.JSONDecodeError:
            results = res.text

        return status, results

    def add_photo_to_pet(self, auth_key: json, pet_id: str, pet_photo) -> json:

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        )

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)

        status = res.status_code
        results = res
        try:
            results = res.json()
        except json.decoder.JSONDecodeError:
            results = res.text

        return status, results

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age, pet_photo):

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code

        results = ""
        try:
            results = res.json()
        except json.decoder.JSONDecodeError:
            results = res.text

        return status, results

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        results = ""
        try:
            results = res.json()
        except json.decoder.JSONDecodeError:
            results = res.text

        return status, results

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        results = ""
        try:
            results = res.json()
        except json.decoder.JSONDecodeError:
            results = res.text

        return status, results


