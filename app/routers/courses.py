from fastapi import HTTPException, APIRouter
import schemas.courses as schemas
from datavalidation import DataValidation
from database import course_collection
from pymongo import ReturnDocument


router = APIRouter()


@router.post("/RegCou/", response_model=schemas.CoursesOut)
async def create_courses(courses: schemas.CoursesCreate):
    """
    Create a new student record
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
async def delete_courses(course_id: str):

    delete_record = course_collection.find_one_and_delete({"cid": course_id})
    if not delete_record:
        raise HTTPException(status_code=400, detail="Course was not deleted")
    else:
        return {"Deleted": True}


@router.patch("/UpdCou/{course_id}", response_model_exclude_unset=True)
async def update_course(course_id: str, course: schemas.CoursesUpdate):

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


@router.get("/GetCou/{course_id}", response_model=schemas.CoursesOut)
async def get_courses(course_id: str):
    record = course_collection.find_one({"cid": course_id})
    if not record:
        raise HTTPException(
            status_code=404, detail="Invalid course id. Course not found"
        )
    return record
