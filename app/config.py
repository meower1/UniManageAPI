"""
Fastapi routers & database integration configs
"""

from os import name
from fastapi import FastAPI
from routers import (
    courses,
    courseregister,
    presentedcourses,
    student,
    lecturer,
    front_page,
)
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(lecturer.router, tags=["lecturer"])
app.include_router(student.router, tags=["student"])
app.include_router(courses.router, tags=["courses"])
app.include_router(courseregister.router, tags=["courseregister"])
app.include_router(presentedcourses.router, tags=["presentedcourses"])
app.include_router(front_page.router, tags=["front page"])
