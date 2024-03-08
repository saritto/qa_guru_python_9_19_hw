import requests
import json
from jsonschema import validate


url = "https://reqres.in/api/users"

headers = {
  'Content-Type': 'application/json',
  'Referer': 'https://reqres.in/',
  'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
  'Sec-Ch-Ua-Mobile': '?0',
  'Sec-Ch-Ua-Platform': '"macOS"'
}


def test_get_single_user():
    response = requests.get(f'{url}/2', headers=headers)
    assert response.status_code == 200
    assert response.json()
    with open("schemas/get_single_status_response.json") as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_post_create():
    payload = {"name": "morpheus", "job": "leader"}
    response = requests.post(url, data=payload)
    assert response.status_code == 201
    assert response.json()
    with open("schemas/post_create_response.json") as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_put_update():
    payload = {"name": "morpheus", "job": "zion resident"}
    response = requests.put(f'{url}/2', data=payload)
    assert response.status_code == 200
    assert response.json()
    with open("schemas/put_update_response.json") as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_delete():
    payload = {"name": "morpheus", "job": "zion resident"}
    response = requests.delete(f'{url}/2', data=payload)
    assert response.status_code == 204


def test_get_not_found():
    payload = {"name": "morpheus", "job": "zion resident"}
    response = requests.get(f'{url}/unknown/2', data=payload)
    assert response.status_code == 404
    assert not response.json()


def test_post_login_unsuccessful():
    payload = {"email": "peter@klaven"}
    response = requests.post('https://reqres.in/api/login', data=payload)
    assert response.status_code == 400
    assert response.json()
    with open("schemas/post_login_unsuccessful_response.json") as file:
        validate(response.json(), schema=json.loads(file.read()))
