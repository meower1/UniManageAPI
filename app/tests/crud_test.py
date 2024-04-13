"""
Tests for CRUD operations on all routers
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

Course_sample = {
    "cid": "12342",
    "cname": "میو",
    "department": "علوم پایه",
    "credit": "3",
}

Lecturer_sample = {
    "lid": "777335",
    "fname": "استاد",
    "lname": "استادیان",
    "id": "3966343916",
    "department": "علوم پایه",
    "major": "مهندسی برق الکترونیک",
    "borncity": "تهران",
    "address": "ویلیام دونی",
    "postalcode": "1231231212",
    "cphone": "09123456789",
    "hphone": "06612121212",
    "lcourseids": [12342],
    "birth": "1383/11/01",
}

Lecturer_out = {
    "lid": "777335",
    "fname": "استاد",
    "lname": "استادیان",
    "department": "علوم پایه",
}

Student_sample = {
    "stid": "40211415035",
    "fname": " میو ماو",
    "lname": "احمد",
    "father": "رضااحمدی",
    "birth": "1401/1/30",
    "ids": "ب/12 123456",
    "address": "میو میو",
    "postalcode": "1234567890",
    "cphone": "09123456789",
    "hphone": "06633223358",
    "major": "مهندسی برق قدرت",
    "married": True,
    "id": "1850527296",
    "scourseids": [12342],
    "lids": [777335],
    "department": "فنی و مهندسی",
    "borncity": "سمنان",
}

Student_out = {
    "stid": "40211415035",
    "fname": " میو ماو",
    "lname": "احمد",
    "father": "رضااحمدی",
}

Courseregister_sample = {
    "cid": "12342",
    "cname": "میوپنچ",
    "department": "علوم پایه",
    "credit": "3",
    "sid": [40211415035],
    "fname": "ویلیام",
    "lname": "رولت",
}

Courseregister_out = {
    "cid": "12342",
    "cname": "میوپنچ",
    "department": "علوم پایه",
    "credit": "3",
}

Courseregister_updated = {
    "cid": "12342",
    "cname": "میوپنچ",
    "department": "فنی و مهندسی",
    "credit": "3",
}


Presentedcourses_sample = {
    "cid": "12342",
    "cname": "میوپنچ",
    "department": "علوم پایه",
    "credit": "3",
    "lid": [777335],
    "fname": "ملکه",
    "lname": "ویلز",
}

Presentedcourses_out = {
    "cid": "12342",
    "cname": "میوپنچ",
    "department": "علوم پایه",
    "credit": "3",
}

Presentedcourses_updated = {
    "cid": "12342",
    "cname": "میوپنچ",
    "department": "فنی و مهندسی",
    "credit": "2",
}


def test_create_courses() -> None:
    """
    Test case for creating a new course
    """
    response = client.post("/RegCou/", json=Course_sample)
    assert response.status_code == 200
    assert response.json() == Course_sample


def test_create_lecturer() -> None:
    """
    Test case for creating a new lecturer
    """
    response = client.post("/RegLec/", json=Lecturer_sample)
    assert response.status_code == 200
    assert response.json() == Lecturer_out


def test_create_students() -> None:
    """
    Test case for creating a new student
    """
    response = client.post("/RegStu/", json=Student_sample)
    assert response.status_code == 200
    assert response.json() == Student_out


def test_create_courseregister() -> None:
    """
    Test case for creating a new course
    """
    response = client.post("/RegCouReg/", json=Courseregister_sample)
    assert response.status_code == 200
    assert response.json() == Courseregister_out


def test_create_presentedcourses() -> None:
    """
    Test case for creating a new course
    """
    response = client.post("/RegPreCou/", json=Presentedcourses_sample)
    assert response.status_code == 200
    assert response.json() == Presentedcourses_out


def test_update_course() -> None:
    """
    Test case for updating a course
    """
    response = client.patch(
        "/UpdCou/12342",
        json={"cname": "میوععع", "department": "فنی و مهندسی", "credit": "2"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "cid": "12342",
        "Updated values:": [
            {"cname": "میوععع", "department": "فنی و مهندسی", "credit": "2"}
        ],
    }


def test_update_lecturer() -> None:
    """
    Test case for updating a lecturer
    """
    response = client.patch(
        "/UpdLec/777335", json={"id": "7064273691", "birth": "1383/11/02"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "lid": "777335",
        "Updated values:": [{"id": "7064273691", "birth": "1383/11/02"}],
    }


def test_update_student() -> None:
    """
    Test case for updating a student
    """
    response = client.patch(
        "/UpdStu/40211415035",
        json={"address": "خیابان سوم", "postalcode": "1234567899"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "stid": "40211415035",
        "Updated values:": [{"address": "خیابان سوم", "postalcode": "1234567899"}],
    }


def test_update_courseregister() -> None:
    """
    Test case for updating a course
    """
    response = client.patch(
        "/UpdCouReg/12342", json={"department": "فنی و مهندسی", "credit": "3"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "cid": "12342",
        "Updated values:": [{"department": "فنی و مهندسی", "credit": "3"}],
    }


def test_update_presentedcourses() -> None:
    """
    Test case for updating a course
    """
    response = client.patch(
        "/UpdPreCou/12342", json={"department": "فنی و مهندسی", "credit": "2"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "cid": "12342",
        "Updated values:": [{"department": "فنی و مهندسی", "credit": "2"}],
    }


def test_get_course() -> None:
    """
    Test case for getting a course
    """
    response = client.get("/GetCou/12342")
    assert response.status_code == 200
    assert response.json() == {
        "cid": "12342",
        "cname": "میوععع",
        "department": "فنی و مهندسی",
        "credit": "2",
    }


def test_get_lecturer() -> None:
    """
    Test case for getting a lecturer
    """
    response = client.get("/GetLec/777335")
    assert response.status_code == 200
    assert response.json() == Lecturer_out


def test_get_student() -> None:
    """
    Test case for getting a student
    """
    response = client.get("/GetStu/40211415035")
    assert response.status_code == 200
    assert response.json() == Student_out


def test_get_courseregister() -> None:
    """
    Test case for getting a course
    """
    response = client.get("/GetCouReg/12342")
    assert response.status_code == 200
    assert response.json() == Courseregister_updated


def test_get_presentedcourses() -> None:
    """
    Test case for getting a course
    """
    response = client.get("/GetPreCou/12342")
    assert response.status_code == 200
    assert response.json() == Presentedcourses_updated
