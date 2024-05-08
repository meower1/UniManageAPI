"""
Represents the schemas models for the Courses table
"""

from pydantic import BaseModel


class CoursesBase(BaseModel):
    """
    Represents the base schema for courses.
    """

    cid: str
    cname: str
    department: str
    credit: str


class CoursesCreate(CoursesBase):
    """
    Represents a course creation request.

    This class inherits from the `CoursesBase` class and is used to define the schema for creating a new course.

    Attributes:
        Inherits all attributes from the `CoursesBase` class.

    """


class CoursesOut(BaseModel):
    """
    Represents the output model for the Courses table.

    Attributes:
        cid (str | None): The course ID.
        cname (str | None): The course name.
        department (str | None): The department of the course.
        credit (str | None): The credit value of the course.
    """

    cid: str | None = None
    cname: str | None = None
    department: str | None = None
    credit: str | None = None


class CoursesUpdate(CoursesBase):
    """
    Represents the schema for updating a course.

    Attributes:
        cid (str | None): The ID of the course. Defaults to None.
        cname (str | None): The name of the course. Defaults to None.
        department (str | None): The department of the course. Defaults to None.
        credit (str | None): The credit of the course. Defaults to None.
    """

    cid: str | None = None
    cname: str | None = None
    department: str | None = None
    credit: str | None = None
