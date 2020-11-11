import requests, json
from uuid import uuid4

SERVER_URL = "http://localhost:8000"


def test_get_all_students():
    response = requests.get(f"{SERVER_URL}/student/")
    assert response.status_code == 200


def test_get_student_404():
    response = requests.get(f"{SERVER_URL}/student/{uuid4()}")
    assert response.status_code == 404


def test_create_student():
    create_student = {
        "prn": 908,
        "first_name": "string",
        "middle_name": "string",
        "last_name": "string",
        "mothers_name": "string",
        "date_of_birth": "2020-11-09",
        "address": "string",
        "contant_number": "+91-9819882939",
        "email": "user@example.com",
    }

    expected_response = {
        "prn": 908,
        "first_name": "string",
        "middle_name": "string",
        "last_name": "string",
        "mothers_name": "string",
        "date_of_birth": "2020-11-09",
        "address": "string",
        "contant_number": "+91-9819882939",
        "email": "user@example.com",
        "status": "active",
        "record": "active",
        "history": [],
    }
    response = requests.post(f"{SERVER_URL}/student/", data=json.dumps(create_student))
    assert response.status_code == 201
    json_response = response.json()
    for k, v in expected_response.items():
        assert expected_response[k] == json_response[k]
    assert json_response["id"]
    assert json_response["timestamp"]
