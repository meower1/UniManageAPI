"""
Student router
includes CRUD operations related to student table
"""

from typing import Any
from fastapi import HTTPException, APIRouter
import schemas.student as schemas
from datavalidation import DataValidation
from database import student_collection
from pymongo import ReturnDocument


router = APIRouter()


@router.post("/RegStu/", response_model=schemas.StudentOut)
async def create_student(student: schemas.StudentCreate) -> dict[str, Any]:
    """
    Create a new student.

    Args:
        student (schemas.StudentCreate): The student data to be created.

    Returns:
        dict: The created student data.

    """
    await DataValidation.duplicate_stid_check(student.stid)
    DataValidation.stid_check(student.stid)
    DataValidation.name_check(student.fname)
    DataValidation.name_check(student.lname)
    DataValidation.name_check(student.father)
    DataValidation.birth_check(student.birth)
    DataValidation.ids_check(student.ids)
    DataValidation.borncity_check(student.borncity)
    DataValidation.address_check(student.address)
    DataValidation.postalcode_check(student.postalcode)
    DataValidation.phonenum_check(student.cphone)
    DataValidation.homenum_check(student.hphone)
    DataValidation.department_check(student.department)
    DataValidation.major_check(student.major)
    DataValidation.birth_check(student.birth)
    DataValidation.id_check(student.id)
    await DataValidation.student_lid_exists(student.lids)
    await DataValidation.student_course_exists(student.scourseids)

    course_data = student.model_dump()
    student_collection.insert_one(course_data)

    return course_data


@router.delete("/DelStu/{student_id}", status_code=200)
async def delete_student(student_id: str):
    """
    Delete a student record from the database.

    Args:
        student_id (str): The ID of the student to be deleted.

    Returns:
        dict: A dictionary containing the student ID and a flag indicating if the student was deleted successfully.

    Raises:
        HTTPException: If the student record was not found and deleted.
    """
    delete_record = student_collection.find_one_and_delete({"stid": student_id})
    if not delete_record:
        raise HTTPException(status_code=400, detail="Student was not deleted")
    return {"Student ID": student_id, "Deleted": True}


@router.patch("/UpdStu/{student_id}", response_model_exclude_unset=True)
async def update_student(
    student_id: str, student: schemas.StudentUpdate
) -> dict[str, Any]:
    """
    Update a student's information in the database.

    Args:
        student_id (str): The ID of the student to be updated.
        student (schemas.StudentUpdate): The updated student data.

    Returns:
        dict: A dictionary containing the student ID and the updated values.

    Raises:
        HTTPException: If the student is not found in the database.
    """
    db_student = student_collection.find_one({"stid": student_id})
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_data = student.model_dump(exclude_unset=True)

    validation_methods = {
        "stid": DataValidation.stid_check,
        "fname": DataValidation.name_check,
        "lname": DataValidation.name_check,
        "father": DataValidation.name_check,
        "birth": DataValidation.birth_check,
        "department": DataValidation.department_check,
        "major": DataValidation.major_check,
        "borncity": DataValidation.borncity_check,
        "ids": DataValidation.ids_check,
        "address": DataValidation.address_check,
        "postalcode": DataValidation.postalcode_check,
        "cphone": DataValidation.phonenum_check,
        "hphone": DataValidation.homenum_check,
        "id": DataValidation.id_check,
    }

    # Loops through the updated values and applies the value checks
    # To the existing values
    for attr, validation_method in validation_methods.items():
        if getattr(student, attr):
            validation_method(getattr(student, attr))

    await DataValidation.duplicate_stid_check(student.stid)
    await DataValidation.student_duplicate_lids(student.lids)
    await DataValidation.student_duplicate_scourseids(student.scourseids)
    await DataValidation.student_course_exists(student.scourseids)
    await DataValidation.student_lid_exists(student.lids)

    student_collection.find_one_and_update(
        {"stid": student_id},
        {"$set": student_data},
        return_document=ReturnDocument.AFTER,
    )
    response = {}
    response.update({"stid": student_id})
    response.update({"Updated values:": [student_data]})

    return response


@router.get("/GetStu/{student_id}", response_model=schemas.StudentUpdate)
async def get_student(student_id: str) -> dict[str, Any]:
    """
    Retrieve a student by their ID.

    Args:
        student_id (str): The ID of the student to retrieve.

    Returns:
        dict: The student record.

    Raises:
        HTTPException: If the student with the given ID is not found.
    """
    record = student_collection.find_one({"stid": student_id})
    if not record:
        raise HTTPException(
            status_code=404, detail="Invalid student id. Student not found"
        )
    return record
