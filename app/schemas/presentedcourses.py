from pydantic import BaseModel
from typing import List

# Pydantic is used for data validation in fastapi


class PresentedCoursesBase(BaseModel):
    cid: str
    cname: str
    department: str
    credit: str
    lid: List[int]
    fname: str
    lname: str


class PresentedCoursesCreate(PresentedCoursesBase):
    # Sensitive information that are only needed
    # for user creation

    pass


class PresentedCoursesOut(BaseModel):
    # Changed the class inheritance from PresentedCoursesBase to BaseModel
    # Outputs the first 4 values of Courses table

    cid: str
    cname: str
    department: str
    credit: str


class PresentedCoursesUpdate(PresentedCoursesBase):
    cid: str | None = None
    cname: str | None = None
    department: str | None = None
    credit: str | None = None
    lid: List[int] | None = None
    fname: str | None = None
    lname: str | None = None
