"""
Presented courses router
includes CRUD operations related to presentedcourses table
"""

from typing import Any
from fastapi import HTTPException, APIRouter
import schemas.presentedcourses as schemas
from datavalidation import DataValidation
from database import presentedcourses_collection
from pymongo import ReturnDocument


router = APIRouter()


@router.post("/RegPreCou/", response_model=schemas.PresentedCoursesOut)
async def create_presented_courses(
    courses: schemas.PresentedCoursesCreate,
) -> dict[str, Any]:
    """
    Create a new presented course.

    Args:
        courses (schemas.PresentedCoursesCreate): The data for the new presented course.

    Returns:
        dict[str, Any]: The created presented course data.
    """
    await DataValidation.duplicate_cid_check(courses.cid, presentedcourses_collection)
    await DataValidation.cid_exists(courses.cid)
    await DataValidation.student_lid_exists(courses.lid)
    DataValidation.cid_check(courses.cid)
    DataValidation.name_check_courses(courses.cname)
    DataValidation.department_check(courses.department)
    DataValidation.credit_check(courses.credit)
    DataValidation.name_check(courses.fname)
    DataValidation.name_check(courses.lname)

    course_data = courses.model_dump()
    presentedcourses_collection.insert_one(course_data)

    return course_data


@router.delete("/DelPreCou/{course_id}", status_code=200)
async def delete_courses(course_id: str) -> dict[str, Any]:
    """
    Delete a course by its ID.

    Args:
        course_id (str): The ID of the course to be deleted.

    Returns:
        dict: A dictionary containing the course ID and a flag indicating if the course was deleted successfully.

    Raises:
        HTTPException: If the course was not deleted.
    """
    delete_record = presentedcourses_collection.find_one_and_delete({"cid": course_id})
    if not delete_record:
        raise HTTPException(status_code=400, detail="Course was not deleted")
    return {"Course ID": course_id, "Deleted": True}


@router.patch("/UpdPreCou/{course_id}", response_model_exclude_unset=True)
async def update_course(
    course_id: str, course: schemas.PresentedCoursesUpdate
) -> dict[str, Any]:
    """
    Update a course with the given course_id.

    Args:
        course_id (str): The ID of the course to be updated.
        course (schemas.PresentedCoursesUpdate): The updated course data.

    Returns:
        dict: A dictionary containing the updated course ID and the updated values.

    Raises:
        HTTPException: If the course with the given course_id is not found.
    """

    # Checks to see if cid exists
    db_course = presentedcourses_collection.find_one({"cid": course_id})
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

    # Duplicate cid check
    await DataValidation.duplicate_cid_check(course.cid, presentedcourses_collection)
    await DataValidation.cid_exists(course.cid)
    await DataValidation.student_lid_exists(course.lid)

    presentedcourses_collection.find_one_and_update(
        {"cid": course_id}, {"$set": course_data}, return_document=ReturnDocument.AFTER
    )

    response = {}
    response.update({"cid": course_id})
    response.update({"Updated values:": [course_data]})

    return response


@router.get("/GetPreCou/{course_id}", response_model=schemas.PresentedCoursesUpdate)
async def get_courses(course_id: str) -> dict[str, Any]:
    """
    Retrieve information about a presented course by its course ID.

    Args:
        course_id (str): The ID of the course to retrieve information for.

    Returns:
        dict: The information of the presented course.

    Raises:
        HTTPException: If the course ID is invalid and the course is not found.
    """
    record = presentedcourses_collection.find_one({"cid": course_id})
    if not record:
        raise HTTPException(
            status_code=404, detail="Invalid course id. Course not found"
        )
    return record
