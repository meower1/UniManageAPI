from pydantic import BaseModel
from typing import List

# Pydantic is used for data validation in fastapi


class LecturerBase(BaseModel):
    __tablename__ = "lecturer"

    lid: str
    fname: str
    lname: str
    department: str
    major: str
    birth: str
    borncity: str
    lcourseids: List[int]


class LecturerCreate(LecturerBase):
    # Sensitive information that are only needed
    # for user creation

    id: str
    address: str
    postalcode: str
    cphone: str
    hphone: str


class LecturerOut(BaseModel):
    # Changed the class inheritance from LecturerBase to BaseModel
    # Outputs the first 4 values of Lecturer table

    lid: str
    fname: str
    lname: str
    department: str


class LecturerUpdate(LecturerCreate):

    lid: str | None = None
    fname: str | None = None
    lname: str | None = None
    department: str | None = None
    major: str | None = None
    birth: str | None = None
    borncity: str | None = None
    lcourseids: List[int] | None = None
    id: str | None = None
    address: str | None = None
    postalcode: str | None = None
    cphone: str | None = None
    hphone: str | None = None
