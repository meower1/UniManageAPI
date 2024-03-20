from pydantic import BaseModel

# Pydantic is used for data validation in fastapi


class CoursesBase(BaseModel):
    cid: str
    cname: str
    department: str
    credit: str


class CoursesCreate(CoursesBase):
    # Sensitive information that are only needed
    # for user creation

    pass


class CoursesOut(BaseModel):
    # Changed the class inheritance from CoursesBase to BaseModel
    # Outputs the first 4 values of Courses table

    cid: str | None = None
    cname: str | None = None
    department: str | None = None
    credit: str | None = None


class CoursesUpdate(CoursesBase):
    cid: str | None = None
    cname: str | None = None
    department: str | None = None
    credit: str | None = None
