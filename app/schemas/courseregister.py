"""
Represents the schemas models for the Course register table
"""

from typing import List
from pydantic import BaseModel


class CourseRegisterBase(BaseModel):
    """
    Represents the base schema for course registration.

    Attributes:
        cid (str): The course ID.
        cname (str): The course name.
        department (str): The department of the course.
        credit (str): The credit hours of the course.
        sid (List[int]): The list of student IDs registered for the course.
        fname (str): The first name of the faculty teaching the course.
        lname (str): The last name of the faculty teaching the course.
    """

    cid: str
    cname: str
    department: str
    credit: str
    sid: List[int]
    fname: str
    lname: str


class CourseRegisterCreate(CourseRegisterBase):
    """
    Represents a course registration request for creating a new course registration.

    This class inherits from the `CourseRegisterBase` class and includes sensitive information
    that is only needed for user creation.

    Attributes:
        Inherits all attributes from the `CourseRegisterBase` class.

    """


class CourseRegisterOut(BaseModel):
    """
    Represents the output model for Course registration.

    Attributes:
        cid (str): The ID of the course.
        cname (str): The name of the course.
        department (str): The department of the course.
        credit (str): The credit value of the course.
    """

    cid: str
    cname: str
    department: str
    credit: str


class CourseRegisterUpdate(CourseRegisterBase):
    """
    Represents the data required to update a course registration.

    Attributes:
        cid (str | None): The ID of the course. Defaults to None.
        cname (str | None): The name of the course. Defaults to None.
        department (str | None): The department of the course. Defaults to None.
        credit (str | None): The credit of the course. Defaults to None.
        sid (List[int] | None): The list of student IDs. Defaults to None.
        fname (str | None): The first name of the faculty. Defaults to None.
        lname (str | None): The last name of the faculty. Defaults to None.
    """

    cid: str | None = None
    cname: str | None = None
    department: str | None = None
    credit: str | None = None
    sid: List[int] | None = None
    fname: str | None = None
    lname: str | None = None
