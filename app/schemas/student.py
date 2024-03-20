from pydantic import BaseModel
from typing import List

# Pydantic is used for data validation in fastapi


class StudentBase(BaseModel):
    stid: str
    fname: str
    lname: str
    father: str
    birth: str
    department: str
    major: str
    married: bool
    lids: List[int]
    scourseids: List[int]
    borncity: str


class StudentCreate(StudentBase):
    # Sensitive information that are only needed
    # for user creation

    ids: str
    address: str
    postalcode: str
    cphone: str
    hphone: str
    id: str


class StudentOut(BaseModel):
    # Changed the class inheritance from StudentBase to BaseModel
    # Outputs the first 4 values of student table

    stid: str
    fname: str
    lname: str
    father: str


class StudentUpdate(StudentCreate):
    stid: str | None = None
    fname: str | None = None
    lname: str | None = None
    father: str | None = None
    birth: str | None = None
    department: str | None = None
    major: str | None = None
    married: bool | None = None
    lids: List[int] | None = None
    scourseids: List[int] | None = None
    borncity: str | None = None
    ids: str | None = None
    address: str | None = None
    postalcode: str | None = None
    cphone: str | None = None
    hphone: str | None = None
    id: str | None = None
