import json


def test_create_job(client):
    data = {
        "title": "developer",
        "company": "cdek",
        "company_url": "cdek.com",
        "location": "Россия",
        "descriptions": "Хорошая компания!!! ",
        "date_posted": "2022-07-22"
    }
    response = client.post('/jobs/create-job/', json.dumps(data))
    assert response.status_code == 200
    assert response.json()['company'] == "cdek"
    assert response.json()['company_url'] == "cdek.com"
    assert response.json()['descriptions'] == "Хорошая компания!!! "
    assert response.json()['date_posted'] == "2022-07-22"


def test_read_job(client):
    data = {
        "title": "developer",
        "company": "cdek",
        "company_url": "cdek.com",
        "location": "Россия",
        "descriptions": "Хорошая компания!!! ",
        "date_posted": "2022-07-22"
    }
    response = client.post("/jobs/create-job/", json.dumps(data))

    response = client.get("/jobs/get/1")
    assert response.status_code == 200
    assert response.json()['title'] == "developer"
