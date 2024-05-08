"""
Represents the schemas models for the Presented courses table
"""

from typing import List
from pydantic import BaseModel


class PresentedCoursesBase(BaseModel):
    """
    Represents the base schema for presented courses.

    Attributes:
        cid (str): The course ID.
        cname (str): The course name.
        department (str): The department offering the course.
        credit (str): The credit hours of the course.
        lid (List[int]): The list of instructor IDs.
        fname (str): The first name of the instructor.
        lname (str): The last name of the instructor.
    """

    cid: str
    cname: str
    department: str
    credit: str
    lid: List[int]
    fname: str
    lname: str


class PresentedCoursesCreate(PresentedCoursesBase):
    """
    Represents the schema for creating a presented course.

    This class inherits from `PresentedCoursesBase` and includes any sensitive
    information that is only needed for user creation.

    Attributes:
        Inherits all attributes from `PresentedCoursesBase`.

    """


class PresentedCoursesOut(BaseModel):
    """
    Represents the output schema for the PresentedCourses model.

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


class PresentedCoursesUpdate(PresentedCoursesBase):
    """
    Represents an update for a presented course.

    Attributes:
        cid (str | None): The course ID.
        cname (str | None): The course name.
        department (str | None): The department of the course.
        credit (str | None): The credit value of the course.
        lid (List[int] | None): The list of instructor IDs for the course.
        fname (str | None): The first name of the instructor.
        lname (str | None): The last name of the instructor.
    """

    cid: str | None = None
    cname: str | None = None
    department: str | None = None
    credit: str | None = None
    lid: List[int] | None = None
    fname: str | None = None
    lname: str | None = None
