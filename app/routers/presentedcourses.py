from fastapi import HTTPException, APIRouter
import schemas.presentedcourses as schemas
from datavalidation import DataValidation
from database import presentedcourses_collection
from pymongo import ReturnDocument


router = APIRouter()


@router.post("/RegPreCou/", response_model=schemas.PresentedCoursesOut)
async def create_PresentedCourses(courses: schemas.PresentedCoursesCreate):

    await DataValidation.duplicate_cid_check(courses.cid, presentedcourses_collection)
    await DataValidation.cid_exists(courses.cid)

    # Checks if presentedcourses.lid exists in LID's of lecturer table
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
async def delete_courses(course_id: str):

    delete_record = presentedcourses_collection.find_one_and_delete({"cid": course_id})
    if not delete_record:
        raise HTTPException(status_code=400, detail="Course was not deleted")
    else:
        return {"Deleted": True}


@router.patch("/UpdPreCou/{course_id}", response_model_exclude_unset=True)
async def update_course(course_id: str, course: schemas.PresentedCoursesUpdate):

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


@router.get("/GetPreCou/{course_id}", response_model=schemas.PresentedCoursesOut)
async def get_courses(course_id: str):
    record = presentedcourses_collection.find_one({"cid": course_id})
    if not record:
        raise HTTPException(
            status_code=404, detail="Invalid course id. Course not found"
        )
    return record
