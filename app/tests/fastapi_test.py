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
    "id": "1234467890",
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


# Courses tests


def test_create_courses():
    # Test case for creating a new course
    response = client.post("/RegCou/", json=Course_sample)
    assert response.status_code == 200
    assert response.json() == Course_sample


def test_create_duplicate_course():
    # Test case for creating a duplicate course
    response = client.post("/RegCou/", json=Course_sample)
    assert response.status_code == 409
    assert response.json() == {"detail": "Duplicate course id. Course already exists"}


def test_update_course():
    # Test case for updating a course
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


def test_update_nonexistent_course():
    # Test case for updating a nonexistent course
    response = client.patch("/UpdCou/12349", json=Course_sample)
    assert response.status_code == 404
    assert response.json() == {"detail": "Course not found"}


def test_get_course():
    # Test case for getting a course
    response = client.get("/GetCou/12342")
    assert response.status_code == 200
    assert response.json() == {
        "cid": "12342",
        "cname": "میوععع",
        "department": "فنی و مهندسی",
        "credit": "2",
    }


def test_get_nonexistent_course():
    # Test case for getting a nonexistent course
    response = client.get("/GetCou/12349")
    assert response.status_code == 404

    def test_get_nonexistent_course():
        # Test case for getting a nonexistent course
        response = client.get("/GetCou/12349")
        assert response.status_code == 404
        assert response.json() == {"detail": "Invalid course id. Course not found"}


# Lecturers test


def test_create_lecturer():
    # Test case for creating a new lecturer
    response = client.post("/RegLec/", json=Lecturer_sample)
    assert response.status_code == 200
    assert response.json() == Lecturer_out


def test_create_duplicate_lecturer():
    # Test case for creating a duplicate lecturer
    response = client.post("/RegLec/", json=Lecturer_sample)
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Duplicate lecturer id. lecturer already exists"
    }


def test_update_lecturer():
    # Test case for updating a lecturer
    response = client.patch(
        "/UpdLec/777335", json={"id": "1234467892", "birth": "1383/11/02"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "lid": "777335",
        "Updated values:": [{"id": "1234467892", "birth": "1383/11/02"}],
    }


def test_update_nonexistent_lecturer():
    # Test case for updating a nonexistent lecturer
    response = client.patch("/UpdLec/777336", json=Lecturer_sample)
    assert response.status_code == 404
    assert response.json() == {"detail": "Lecturer not found"}


def test_get_lecturer():
    # Test case for getting a lecturer
    response = client.get("/GetLec/777335")
    assert response.status_code == 200
    assert response.json() == Lecturer_out


def test_get_nonexistent_lecturer():
    # Test case for getting a nonexistent lecturer
    response = client.get("/GetLec/777339")
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid lecturer id. Lecturer not found"}


# Students section


def test_create_students():
    # Test case for creating a new student
    response = client.post("/RegStu/", json=Student_sample)
    assert response.status_code == 200
    assert response.json() == Student_out


def test_create_duplicate_student():
    # Test case for creating a duplicate student
    response = client.post("/RegStu/", json=Student_sample)
    assert response.status_code == 409
    assert response.json() == {"detail": "Duplicate student id. Student already exists"}


def test_update_student():
    # Test case for updating a student
    response = client.patch(
        "/UpdStu/40211415035",
        json={"address": "خیابان سوم", "postalcode": "1234567899"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "stid": "40211415035",
        "Updated values:": [{"address": "خیابان سوم", "postalcode": "1234567899"}],
    }


def test_update_nonexistent_student():
    # Test case for updating a nonexistent student
    response = client.patch("/UpdStu/40211415039", json=Student_sample)
    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}


def test_get_student():
    # Test case for getting a student
    response = client.get("/GetStu/40211415035")
    assert response.status_code == 200
    assert response.json() == Student_out


def test_get_nonexistent_student():
    # Test case for getting a nonexistent student
    response = client.get("/GetStu/40211415039")
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid student id. Student not found"}


# Courseregister section


def test_create_courseregister():
    # Test case for creating a new course
    response = client.post("/RegCouReg/", json=Courseregister_sample)
    assert response.status_code == 200
    assert response.json() == Courseregister_out


def test_create_duplicate_courseregister():
    # Test case for creating a duplicate course
    response = client.post("/RegCouReg/", json=Courseregister_sample)
    assert response.status_code == 409
    assert response.json() == {"detail": "Duplicate course id. Course already exists"}


def test_get_courseregister():
    # Test case for getting a course
    response = client.get("/GetCouReg/12342")
    assert response.status_code == 200
    assert response.json() == Courseregister_out


def test_get_nonexistent_courseregister():
    # Test case for getting a nonexistent course
    response = client.get("/GetCouReg/12349")
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid course id. Course not found"}


def test_update_courseregister():
    # Test case for updating a course
    response = client.patch(
        "/UpdCouReg/12342", json={"department": "فنی و مهندسی", "credit": "3"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "cid": "12342",
        "Updated values:": [{"department": "فنی و مهندسی", "credit": "3"}],
    }


def test_update_nonexistent_courseregister():
    # Test case for updating a nonexistent course
    response = client.patch("/UpdCouReg/12349", json=Courseregister_sample)
    assert response.status_code == 404
    assert response.json() == {"detail": "Course not found"}


# PresentedCourses section


def test_create_presentedcourses():
    # Test case for creating a new course
    response = client.post("/RegPreCou/", json=Presentedcourses_sample)
    assert response.status_code == 200
    assert response.json() == Presentedcourses_out


def test_create_duplicate_presentedcourses():
    # Test case for creating a duplicate course
    response = client.post("/RegPreCou/", json=Presentedcourses_sample)
    assert response.status_code == 409
    assert response.json() == {"detail": "Duplicate course id. Course already exists"}


def test_get_presentedcourses():
    # Test case for getting a course
    response = client.get("/GetPreCou/12342")
    assert response.status_code == 200
    assert response.json() == Presentedcourses_out


def test_get_nonexistent_presentedcourses():
    # Test case for getting a nonexistent course
    response = client.get("/GetPreCou/12349")
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid course id. Course not found"}


def test_update_presentedcourses():
    # Test case for updating a course
    response = client.patch(
        "/UpdPreCou/12342", json={"department": "فنی و مهندسی", "credit": "2"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "cid": "12342",
        "Updated values:": [{"department": "فنی و مهندسی", "credit": "2"}],
    }


def test_update_nonexistent_presentedcourses():
    # Test case for updating a nonexistent course
    response = client.patch("/UpdPreCou/12349", json=Presentedcourses_sample)
    assert response.status_code == 404
    assert response.json() == {"detail": "Course not found"}


# Record deletion
def test_delete_course():
    # Test case for deleting a course
    response = client.delete("/DelCou/12342")
    assert response.status_code == 200
    assert response.json() == {"Deleted": True}


def test_delete_nonexistent_course():
    # Test case for deleting a nonexistent course
    response = client.delete("/DelCou/12349")
    assert response.status_code == 400
    assert response.json() == {"detail": "Course was not deleted"}


def test_delete_lecturer():
    # Test case for deleting a lecturer
    response = client.delete("/DelLec/777335")
    assert response.status_code == 200
    assert response.json() == {"Deleted": True}


def test_delete_nonexistent_lecturer():
    # Test case for deleting a nonexistent lecturer
    response = client.delete("/DelLec/777336")
    assert response.status_code == 400
    assert response.json() == {"detail": "Lecturer was not deleted"}


def test_delete_student():
    # Test case for deleting a student
    response = client.delete("/DelStu/40211415035")
    assert response.status_code == 200
    assert response.json() == {"Deleted": True}


def test_delete_nonexistent_student():
    # Test case for deleting a student
    response = client.delete("/DelStu/40211415039")
    assert response.status_code == 400
    assert response.json() == {"detail": "Student was not deleted"}


def test_delete_courseregister():
    # Test case for deleting a course
    response = client.delete("/DelCouReg/12342")
    assert response.status_code == 200
    assert response.json() == {"Deleted": True}


def test_delete_nonexistent_courseregister():
    # Test case for deleting a nonexistent course
    response = client.delete("/DelCou/12349")
    assert response.status_code == 400
    assert response.json() == {"detail": "Course was not deleted"}


def test_delete_presentedcourses():
    # Test case for deleting a course
    response = client.delete("/DelPreCou/12342")
    assert response.status_code == 200
    assert response.json() == {"Deleted": True}


def test_delete_nonexistent_presentedcourses():
    # Test case for deleting a nonexistent course
    response = client.delete("/DelPreCou/12349")
    assert response.status_code == 400
    assert response.json() == {"detail": "Course was not deleted"}
