from typing import List
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from server.database import retrieve_courses, insert_course
from server.schemas.common import Message, RecordStatus, ResponseException
from server.schemas.student import Student, StudentDB, UpdateStudent
from server.schemas.subjects import Subject
from server.schemas.courses import Course

router = APIRouter()


@router.get("/", response_model=List[Course])
async def get_all_courses():
    courses = await retrieve_courses()
    return courses


@router.post("/", response_model=Course)
async def add_course(course: Course):
    added_course = await insert_course(jsonable_encoder(course))
    return added_course
