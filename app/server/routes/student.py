from typing import List, Union

from fastapi import APIRouter, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from server.database import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student,
)
from server.models.student import Student, StudentDB, UpdateStudent
from server.models.student_1 import (
    ErrorResponseModel,
    ResponseModel,
    UpdateStudentModel,
)
from server.models.common import ResponseModel, Message

router = APIRouter()


@router.post(
    "/",
    response_model=StudentDB,
    status_code=status.HTTP_201_CREATED,
    response_description="Student data added into the database",
)
async def add_student_data(student: Student = Body(...)):
    student_response = jsonable_encoder(StudentDB(**student.dict()))
    created_student = await add_student(student_response)
    return created_student


@router.get(
    "/", response_model=List[StudentDB], response_description="Students retrieved"
)
async def get_students():
    students = await retrieve_students()
    if students:
        return students
    raise HTTPException(status_code=status.HTTP_200_OK, detail="No Students present")


@router.get(
    "/{id}",
    response_model=StudentDB,
    responses={status.HTTP_404_NOT_FOUND: {"model": Message}},
    response_description="Student data retrieved",
)
async def get_student_data(id):
    student = await retrieve_student(id)
    if student:
        return student
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"Student with {id} does not exist"},
    )


@router.put(
    "/{id}",
    response_model=StudentDB,
    responses={status.HTTP_404_NOT_FOUND: {"model": Message}},
)
async def update_student_data(id: str, req: UpdateStudent = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_student(id, req)
    if updated_student:
        return updated_student
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"Student {id} not found"},
    )


@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str):
    deleted_student = await delete_student(id)
    if deleted_student:
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Student with id {0} doesn't exist".format(id)
    )
