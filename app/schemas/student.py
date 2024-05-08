"""
Represents the schemas models for the Student table
"""

from typing import List
from pydantic import BaseModel


class StudentBase(BaseModel):
    """
    Represents the base schema for a student.

    Attributes:
        stid (str): The student ID.
        fname (str): The first name of the student.
        lname (str): The last name of the student.
        father (str): The name of the student's father.
        birth (str): The birth date of the student.
        department (str): The department of the student.
        major (str): The major of the student.
        married (bool): Indicates whether the student is married or not.
        lids (List[int]): A list of IDs representing the student's courses.
        scourseids (List[int]): A list of IDs representing the student's selected courses.
        borncity (str): The city where the student was born.
    """

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
    """
    Represents a student object used for user creation.

    Attributes:
        ids (str): The student's identification number.
        address (str): The student's address.
        postalcode (str): The student's postal code.
        cphone (str): The student's contact phone number.
        hphone (str): The student's home phone number.
        id (str): The student's ID.
    """

    ids: str
    address: str
    postalcode: str
    cphone: str
    hphone: str
    id: str


class StudentOut(BaseModel):
    """
    Represents the output model for a student.

    Attributes:
        stid (str): The student ID.
        fname (str): The first name of the student.
        lname (str): The last name of the student.
        father (str): The name of the student's father.
    """

    stid: str
    fname: str
    lname: str
    father: str


class StudentUpdate(StudentCreate):
    """
    Represents the schema for updating a student's information.
    """

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
