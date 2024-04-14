"""
Course register router
includes CRUD operations related to courseregister table
"""

from typing import Any
from fastapi import HTTPException, APIRouter
import schemas.courseregister as schemas
from datavalidation import DataValidation
from database import courseregister_collection
from pymongo import ReturnDocument


router = APIRouter()


@router.post("/RegCouReg/", response_model=schemas.CourseRegisterOut)
async def create_courseregister(
    courses: schemas.CourseRegisterCreate,
) -> dict[str, Any]:
    """
    Create a new course registration.

    Args:
        courses (schemas.CourseRegisterCreate): The course registration data.

    Returns:
        dict[str, Any]: The created course registration data.
    """

    await DataValidation.duplicate_cid_check(courses.cid, courseregister_collection)
    await DataValidation.cid_exists(courses.cid)
    await DataValidation.stid_exists(courses.sid)
    DataValidation.cid_check(courses.cid)
    DataValidation.name_check_courses(courses.cname)
    DataValidation.department_check(courses.department)
    DataValidation.credit_check(courses.credit)
    DataValidation.name_check(courses.fname)
    DataValidation.name_check(courses.lname)

    course_data = courses.model_dump()
    courseregister_collection.insert_one(course_data)

    return course_data


@router.delete("/DelCouReg/{course_id}", status_code=200)
async def delete_courses(course_id: str) -> dict[str, Any]:
    """
    Delete a course registration record by its ID.

    Parameters:
    - course_id (str): The ID of the course registration record to delete.

    Returns:
    - dict[str, Any]: A dictionary containing the course ID and a flag indicating if the deletion was successful.

    Raises:
    - HTTPException: If the course registration record was not found and deleted.
    """
    delete_record = courseregister_collection.find_one_and_delete({"cid": course_id})
    if not delete_record:
        raise HTTPException(status_code=400, detail="Course was not deleted")
    return {"Course ID": course_id, "Deleted": True}


@router.patch("/UpdCouReg/{course_id}", response_model_exclude_unset=True)
async def update_course(
    course_id: str, course: schemas.CourseRegisterUpdate
) -> dict[str, Any]:
    """
    Update a course in the course register table.

    Args:
        course_id (str): The ID of the course to be updated.
        course (CourseRegisterUpdate): The updated course data.

    Returns:
        dict[str, Any]: A dictionary containing the updated course ID and the updated values.

    Raises:
        HTTPException: If the course is not found.
    """

    db_course = courseregister_collection.find_one({"cid": course_id})
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    course_data = course.model_dump(exclude_unset=True)

    validation_methods = {
        "cid": DataValidation.cid_check,
        "cname": DataValidation.name_check_courses,
        "department": DataValidation.department_check,
        "credit": DataValidation.credit_check,
        "fname": DataValidation.name_check,
        "lname": DataValidation.name_check,
    }

    for attr, validation_method in validation_methods.items():
        if getattr(course, attr) is not None:
            validation_method(getattr(course, attr))

    await DataValidation.duplicate_cid_check(course.cid, courseregister_collection)
    await DataValidation.cid_exists(course.cid)
    await DataValidation.stid_exists(course.sid)

    courseregister_collection.find_one_and_update(
        {"cid": course_id}, {"$set": course_data}, return_document=ReturnDocument.AFTER
    )

    # Beautifying the output
    response = {}
    response.update({"cid": course_id})
    response.update({"Updated values:": [course_data]})

    return response


@router.get("/GetCouReg/{course_id}", response_model=schemas.CourseRegisterUpdate)
async def get_courses(course_id: str) -> dict[str, Any]:
    """
    Retrieve course registration details by course ID.

    Args:
        course_id (str): The ID of the course to retrieve.

    Returns:
        dict[str, Any]: The course registration details.

    Raises:
        HTTPException: If the course ID is invalid and the course is not found.
    """
    record = courseregister_collection.find_one({"cid": course_id})
    if not record:
        raise HTTPException(
            status_code=404, detail="Invalid course id. Course not found"
        )
    return record
