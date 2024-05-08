"""
Lecturer router
includes CRUD operations related to lecturer table
"""

from typing import Any
from fastapi import HTTPException, APIRouter
import schemas.lecturer as schemas
from datavalidation import DataValidation
from database import lecturer_collection
from pymongo import ReturnDocument


router = APIRouter()


@router.post("/RegLec/", response_model=schemas.LecturerOut)
async def create_lecturer(lecturer: schemas.LecturerCreate) -> dict[str, Any]:
    """
    Create a new lecturer.

    Args:
        lecturer (schemas.LecturerCreate): The data of the lecturer to be created.

    Returns:
        dict: The data of the created lecturer.
    """
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

    lecturer_data = lecturer.model_dump()
    lecturer_collection.insert_one(lecturer_data)

    return lecturer_data


@router.delete("/DelLec/{lecturer_id}", status_code=200)
async def delete_lecturer(lecturer_id: str) -> dict[str, Any]:
    """
    Delete a lecturer record from the database.

    Args:
        lecturer_id (str): The ID of the lecturer to be deleted.

    Returns:
        dict: A dictionary containing the lecturer ID and a flag indicating if the deletion was successful.

    Raises:
        HTTPException: If the lecturer was not found and deleted.
    """
    delete_record = lecturer_collection.find_one_and_delete({"lid": lecturer_id})
    if not delete_record:
        raise HTTPException(status_code=400, detail="Lecturer was not deleted")
    return {"Lecturer ID": lecturer_id, "Deleted": True}


@router.patch("/UpdLec/{lecturer_id}", response_model_exclude_unset=True)
async def update_lecturer(
    lecturer_id: str, lecturer: schemas.LecturerUpdate
) -> dict[str, Any]:
    """
    Update a lecturer's information in the database.

    Args:
        lecturer_id (str): The ID of the lecturer to be updated.
        lecturer (schemas.LecturerUpdate): The updated lecturer data.

    Returns:
        dict: A dictionary containing the updated lecturer ID and the updated values.

    Raises:
        HTTPException: If the lecturer with the given ID is not found in the database.
    """
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

    # Checks for duplicate lid in the database
    await DataValidation.duplicate_lid_check(lecturer.lid)

    # Checks to see if courses assigned to a lecturer exist in courses list
    # Inside the database after update
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


@router.get("/GetLec/{lecturer_id}", response_model=schemas.LecturerUpdate)
async def get_lecturer(lecturer_id: str) -> dict[str, Any]:
    """
    Retrieve a lecturer by their ID.

    Args:
        lecturer_id (str): The ID of the lecturer to retrieve.

    Returns:
        dict: The details of the lecturer.

    Raises:
        HTTPException: If the lecturer with the given ID is not found.
    """
    record = lecturer_collection.find_one({"lid": lecturer_id})
    if not record:
        raise HTTPException(
            status_code=404, detail="Invalid lecturer id. Lecturer not found"
        )
    return record
