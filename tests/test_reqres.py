import requests
import json
from jsonschema import validate
from pathlib import Path


url = "https://reqres.in/api/users"


def schema_path(name):
    return str(Path(__file__).parent.parent.joinpath(f'schemas/{name}'))


def test_get_single_user():
    response = requests.get(f'{url}/2')
    assert response.status_code == 200
    schema = schema_path("get_single_status_response.json")
    with open(schema) as file:
        validate(response.json(), schema=json.loads(file.read()))


def test_post_create():
    name = "morpheus"
    job = "leader"
    payload = {"name": name, "job": job}
    response = requests.post(url, data=payload)
    assert response.status_code == 201
    schema = schema_path("post_create_response.json")
    with open(schema) as file:
        validate(response.json(), schema=json.loads(file.read()))
    assert response.json()["name"] == name
    assert response.json()["job"] == job


def test_put_update():
    name = "morpheus"
    job = "zion resident"
    payload = {"name": name, "job": job}
    response = requests.put(f'{url}/2', data=payload)
    assert response.status_code == 200
    schema = schema_path("put_update_response.json")
    with open(schema) as file:
        validate(response.json(), schema=json.loads(file.read()))
    assert response.json()["name"] == name
    assert response.json()["job"] == job


def test_delete():
    payload = {"name": "morpheus", "job": "zion resident"}
    response = requests.delete(f'{url}/2', data=payload)
    assert response.status_code == 204
    assert response.text == ''


def test_get_not_found():
    payload = {"name": "morpheus", "job": "zion resident"}
    response = requests.get(f'{url}/unknown/2', data=payload)
    assert response.status_code == 404
    assert response.json() == {}


def test_post_login_unsuccessful():
    payload = {"email": "peter@klaven"}
    response = requests.post('https://reqres.in/api/login', data=payload)
    assert response.status_code == 400
    schema = schema_path("post_login_unsuccessful_response.json")
    with open(schema) as file:
        validate(response.json(), schema=json.loads(file.read()))
    assert response.json() == {"error": "Missing password"}
