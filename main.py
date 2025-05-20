from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {1: {"name": "John Doe", "age": 20, "major": "Computer Science"}}

courses = {1: {"subject": "machine learning", "time": 40}}


class Student(BaseModel):
    name: str
    age: int
    major: str


class Course(BaseModel):
    subject: str
    time: int


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[str] = None
    major: Optional[str] = None


# Define a simple GET endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/students/{student_id}")
async def get_student(
    student_id: int = Path(..., title="The ID of the student to get", gt=0)
):
    return students[student_id]


@app.get("/students/{student_id}/name")
async def get_students_name(
    *, student_id: int, name: Optional[str] = None, number: int
):
    # return the value when the name matches
    if name:
        for v in students.values():
            if v["name"] == name:
                return v


@app.post("/students/{student_id}")
async def create_student(student_id: int, student: Student, number: int = 0):
    if student_id in students:
        return {"Error": "student exists"}
    student_dict = student.model_dump()
    students[student_id] = student_dict
    return students[student_id]


@app.post("/classes/{class_id}")
async def create_class(class_id: int, course: Course):
    if class_id in courses:
        return {"Error": "course exists"}
    course_dict = course.model_dump()
    courses[class_id] = course_dict
    return courses[class_id]


@app.put("/students/{student_id}")
async def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Not a student id"}
    students[student_id] = student.model_dump()
    return students[student_id]


@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not existt"}
    del students[student_id]
