from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import Union, List
from datetime import datetime

app =  FastAPI()
studentList = {}

class Content(BaseModel):
    name: str
    description: str


class Subject(BaseModel):
    name: str
    level: int
    creditUnits: int
    price: float
    description: str
    content: Union[List[Content], None] = None
    

class Student(BaseModel):
    name: str
    lastname: str
    birthDate: datetime
    phoneNumber: str
    address: str
    academicRecord: Union[List[Subject], None] = None

class StudentDB(Student):
    id: str

    @field_validator('id')
    def validate_id(id):
        if id in studentList:
            raise HTTPException(status_code=400, detail="ID Already in use")
        return id

class Institute(BaseModel):
    students: List[Student]
    

@app.post('/student')
async def post_student(student: Student):
    return {"Student": student}

@app.post('/institute')
async def post_institute(institute: Institute):
    return {"Institute": institute}

@app.get('/student/list')
async def get_student_list():
    return {"Student List": studentList}

@app.post('/student/create')
async def create_student(student: StudentDB):
    newStudent = Student(**(dict(student)))
    studentList.update({student.id: newStudent})
    return newStudent

@app.put('/student/update/{studentID}')
async def update_student(studentID: str, student: Student):
    studentList.update({studentID: student})
    return {"New Student": student}

@app.get('/student/{studentID}')
async def get_student_id(studentID: str):
    return {"student": studentList[studentID]}

@app.delete('/student/delete/{studentID}')
async def update_student(studentID: str):
    del(studentList[studentID])
    return {"Message": "Student Deleted Succesfully"}