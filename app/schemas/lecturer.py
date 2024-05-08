"""
Represents the schemas models for the Lecturer table
"""

from typing import List
from pydantic import BaseModel


class LecturerBase(BaseModel):
    """
    Represents the base schema for a lecturer.

    Attributes:
        lid (str): The unique identifier for the lecturer.
        fname (str): The first name of the lecturer.
        lname (str): The last name of the lecturer.
        department (str): The department the lecturer belongs to.
        major (str): The major of the lecturer.
        birth (str): The birth date of the lecturer.
        borncity (str): The city where the lecturer was born.
        lcourseids (List[int]): A list of course IDs associated with the lecturer.
    """

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
    """
    Represents a lecturer's information needed for user creation.

    Attributes:
        id (str): The ID of the lecturer.
        address (str): The address of the lecturer.
        postalcode (str): The postal code of the lecturer's address.
        cphone (str): The contact phone number of the lecturer.
        hphone (str): The home phone number of the lecturer.
    """

    id: str
    address: str
    postalcode: str
    cphone: str
    hphone: str


class LecturerOut(BaseModel):
    """
    Represents the output model for a lecturer.

    Attributes:
        lid (str): The lecturer's ID.
        fname (str): The lecturer's first name.
        lname (str): The lecturer's last name.
        department (str): The lecturer's department.
    """

    lid: str
    fname: str
    lname: str
    department: str


class LecturerUpdate(LecturerCreate):
    """
    Represents the schema for updating a lecturer.

    Attributes:
        lid (str | None): The lecturer ID.
        fname (str | None): The first name of the lecturer.
        lname (str | None): The last name of the lecturer.
        department (str | None): The department of the lecturer.
        major (str | None): The major of the lecturer.
        birth (str | None): The birth date of the lecturer.
        borncity (str | None): The birth city of the lecturer.
        lcourseids (List[int] | None): The list of course IDs associated with the lecturer.
        id (str | None): The ID of the lecturer.
        address (str | None): The address of the lecturer.
        postalcode (str | None): The postal code of the lecturer.
        cphone (str | None): The contact phone number of the lecturer.
        hphone (str | None): The home phone number of the lecturer.
    """

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
