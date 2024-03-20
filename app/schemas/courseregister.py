from pydantic import BaseModel
from typing import List

# Pydantic is used for data validation in fastapi


class CourseRegisterBase(BaseModel):
    cid: str
    cname: str
    department: str
    credit: str
    sid: List[int]
    fname: str
    lname: str


class CourseRegisterCreate(CourseRegisterBase):
    # Sensitive information that are only needed
    # for user creation

    pass


class CourseRegisterOut(BaseModel):
    # Changed the class inheritance from CourseRegisterBase to BaseModel
    # Outputs the first 4 values of Courses table

    cid: str
    cname: str
    department: str
    credit: str


class CourseRegisterUpdate(CourseRegisterBase):
    cid: str | None = None
    cname: str | None = None
    department: str | None = None
    credit: str | None = None
    sid: List[int] | None = None
    fname: str | None = None
    lname: str | None = None
