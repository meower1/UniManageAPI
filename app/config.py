"""
Fastapi routers & database integration configs
"""

from fastapi import FastAPI
from routers import courses, courseregister, presentedcourses, student, lecturer


app = FastAPI()
app.include_router(lecturer.router, tags=["lecturer"])
app.include_router(student.router, tags=["student"])
app.include_router(courses.router, tags=["courses"])
app.include_router(courseregister.router, tags=["courseregister"])
app.include_router(presentedcourses.router, tags=["presentedcourses"])
