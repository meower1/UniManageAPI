"""
Courses router
includes CRUD operations related to courses table
"""

from typing import Any, Optional
from fastapi import Form, HTTPException, APIRouter, Request
from pytest import TempPathFactory
import schemas.courses as schemas
from datavalidation import DataValidation
from database import course_collection
from pymongo import ReturnDocument
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/GetCou/")
async def get_html(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/RegCou/", response_model=schemas.CoursesOut)
async def create_courses(courses: schemas.CoursesCreate) -> dict[str, Any]:
    """
    Create a new course.

    Args:
        courses (schemas.CoursesCreate): The course data to be created.

    Returns:
        dict: The created course data.

    Raises:
        DuplicateCIDError: If the course ID already exists.
        InvalidCIDError: If the course ID is invalid.
        InvalidNameError: If the course name is invalid.
        InvalidDepartmentError: If the department is invalid.
        InvalidCreditError: If the credit value is invalid.
    """
    await DataValidation.duplicate_cid_check(courses.cid, course_collection)
    DataValidation.cid_check(courses.cid)
    DataValidation.name_check_courses(courses.cname)
    DataValidation.department_check(courses.department)
    DataValidation.credit_check(courses.credit)

    course_data = courses.model_dump()
    course_collection.insert_one(course_data)

    return course_data


@router.delete("/DelCou/{course_id}", status_code=200)
async def delete_courses(course_id: str) -> dict[str, Any]:
    """
    Delete a course from the database.

    Args:
        course_id (str): The ID of the course to be deleted.

    Returns:
        dict[str, Any]: A dictionary containing the course ID and a flag indicating if the course was deleted.

    Raises:
        HTTPException: If the course was not found and deleted.
    """

    delete_record = course_collection.find_one_and_delete({"cid": course_id})
    if not delete_record:
        raise HTTPException(status_code=400, detail="Course was not deleted")
    return {"Course ID": course_id, "Deleted": True}


@router.patch("/UpdCou/{course_id}", response_model_exclude_unset=True)
async def update_course(
    course_id: str, course: schemas.CoursesUpdate
) -> dict[str, Any]:
    """
    Update a course with the given course_id.

    Args:
        course_id (str): The ID of the course to be updated.
        course (schemas.CoursesUpdate): The updated course data.

    Returns:
        dict[str, Any]: A dictionary containing the updated course ID and the updated values.

    Raises:
        HTTPException: If the course with the given course_id is not found.
    """

    course_exists = course_collection.find_one({"cid": course_id})
    if not course_exists:
        raise HTTPException(status_code=404, detail="Course not found")

    course_data = course.model_dump(exclude_unset=True)

    validation_methods = {
        "cid": DataValidation.cid_check,
        "cname": DataValidation.name_check_courses,
        "department": DataValidation.department_check,
        "credit": DataValidation.credit_check,
    }

    for attr, validation_method in validation_methods.items():
        if getattr(course, attr):
            validation_method(getattr(course, attr))

    if course.cid is not None:
        await DataValidation.duplicate_cid_check(course.cid, course_collection)

    course_collection.find_one_and_update(
        {"cid": course_id}, {"$set": course_data}, return_document=ReturnDocument.AFTER
    )

    # Beautifying the response
    response = {}
    response.update({"cid": course_id})
    response.update({"Updated values:": [course_data]})

    return response


@router.get("/GetCou/{course_id}", response_model=schemas.CoursesUpdate)
async def get_courses(course_id: str, request: Request) -> dict[str, Any]:
    """
    Retrieve a course by its ID.

    Args:
        course_id (str): The ID of the course to retrieve.

    Returns:
        dict[str, Any]: The course record.

    Raises:
        HTTPException: If the course with the given ID is not found.
    """

    record = course_collection.find_one({"cid": course_id})

    if not record:
        raise HTTPException(
            status_code=404, detail="Invalid course id. Course not found"
        )

    return record


@router.get("/search_course")
async def search_course(course_id: str, request: Request):

    if not course_id:
        raise HTTPException(status_code=404, detail="Invalid course id")

    record = course_collection.find_one({"cid": course_id}, {"_id": 0})
    return templates.TemplateResponse(
        "get.html", {"request": request, "record": record}
    )


@router.get("/delete_course")
async def delete_course_html(course_id: str, request: Request):

    delete_record = course_collection.find_one_and_delete({"cid": course_id})
    if not delete_record:
        raise HTTPException(status_code=400, detail="Course was not deleted")

    return {"detail": "Record has been deleted"}


@router.post("/create_course_html")
async def create_course_html(
    request: Request,
    course_id: str = Form(...),
    cname: str = Form(...),
    department: str = Form(...),
    credit: str = Form(...),
):
    await DataValidation.duplicate_cid_check(course_id, course_collection)
    DataValidation.cid_check(course_id)
    DataValidation.name_check_courses(cname)
    DataValidation.department_check(department)
    DataValidation.credit_check(credit)
    course_collection.insert_one(
        {
            "cid": course_id,
            "cname": cname,
            "department": department,
            "credit": credit,
        }
    )

    result = course_collection.find_one({"cid": course_id}, {"_id": 0})

    return templates.TemplateResponse(
        "get.html", {"request": request, "record": result}
    )
