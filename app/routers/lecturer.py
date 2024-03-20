from fastapi import HTTPException, APIRouter
import schemas.lecturer as schemas
from datavalidation import DataValidation
from database import lecturer_collection
from pymongo import ReturnDocument


router = APIRouter()


@router.post("/RegLec/", response_model=schemas.LecturerOut)
async def create_Lecturer(lecturer: schemas.LecturerCreate):

    await DataValidation.duplicate_lid_check(lecturer.lid)
    DataValidation.lid_check(lecturer.lid)
    DataValidation.name_check(lecturer.fname)
    DataValidation.name_check(lecturer.lname)
    DataValidation.birth_check(lecturer.birth)
    DataValidation.borncity_check(lecturer.borncity)
    DataValidation.address_check(lecturer.address)
    DataValidation.postalcode_check(lecturer.postalcode)
    DataValidation.phonenum_check(lecturer.cphone)
    DataValidation.homenum_check(lecturer.hphone)
    DataValidation.department_check(lecturer.department)
    DataValidation.major_check(lecturer.major)
    DataValidation.birth_check(lecturer.birth)
    DataValidation.id_check(lecturer.id)
    await DataValidation.lcourseids_exist(lecturer.lcourseids)

    # Beautifying the output
    lecturer_data = lecturer.model_dump()
    lecturer_collection.insert_one(lecturer_data)

    return lecturer_data


@router.delete("/DelLec/{lecturer_id}", status_code=200)
async def delete_lecturer(lecturer_id: str):

    delete_record = lecturer_collection.find_one_and_delete({"lid": lecturer_id})
    if not delete_record:
        raise HTTPException(status_code=400, detail="Lecturer was not deleted")
    else:
        return {"Deleted": True}


@router.patch("/UpdLec/{lecturer_id}", response_model_exclude_unset=True)
async def update_lecturer(lecturer_id: str, lecturer: schemas.LecturerUpdate):

    # Checking if updated LID exists
    db_lecturer = lecturer_collection.find_one({"lid": lecturer_id})
    if not db_lecturer:
        raise HTTPException(status_code=404, detail="Lecturer not found")

    lecturer_data = lecturer.model_dump(exclude_unset=True)

    validation_methods = {
        "lid": DataValidation.lid_check,
        "fname": DataValidation.name_check,
        "lname": DataValidation.name_check,
        "birth": DataValidation.birth_check,
        "department": DataValidation.department_check,
        "major": DataValidation.major_check,
        "borncity": DataValidation.borncity_check,
        "address": DataValidation.address_check,
        "postalcode": DataValidation.postalcode_check,
        "cphone": DataValidation.phonenum_check,
        "hphone": DataValidation.homenum_check,
        "id": DataValidation.id_check,
    }

    for attr, validation_method in validation_methods.items():
        if getattr(lecturer, attr) is not None:
            validation_method(getattr(lecturer, attr))

    # Duplicate lid check
    await DataValidation.duplicate_lid_check(lecturer.lid)

    # Checks to see if courses assigned to a lecturer exist in courses list after update
    if lecturer.lcourseids is not None:
        await DataValidation.lcourseids_exist(lecturer.lcourseids)

    lecturer_collection.find_one_and_update(
        {"lid": lecturer_id},
        {"$set": lecturer_data},
        return_document=ReturnDocument.AFTER,
    )

    response = {}
    response.update({"lid": lecturer_id})
    response.update({"Updated values:": [lecturer_data]})

    return response


@router.get("/GetLec/{lecturer_id}", response_model=schemas.LecturerOut)
async def get_lecturer(lecturer_id: str):
    record = lecturer_collection.find_one({"lid": lecturer_id})
    if not record:
        raise HTTPException(
            status_code=404, detail="Invalid lecturer id. Lecturer not found"
        )
    return record
