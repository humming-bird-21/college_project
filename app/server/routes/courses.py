from typing import List
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from server.database import (
    retrieve_courses,
    insert_course,
    course_collection,
    update_course,
)
from server.schemas.courses import Course, UpdateCourse

router = APIRouter()


async def precondition_subject_by_code(subject: dict):
    course_from_db = await course_collection.find_one(
        {"course_code": subject["course_code"]}
    )
    if course_from_db:
        raise HTTPException(
            status_code=412,
            detail=f"Course with same Course Code ({course_from_db['course_code']}) already present",
        )
    return False


@router.get("/", response_model=List[Course])
async def get_all_courses():
    courses = await retrieve_courses()
    return courses


@router.post("/", response_model=Course)
async def add_course(course: Course):
    await precondition_subject_by_code(jsonable_encoder(course))
    added_course = await insert_course(jsonable_encoder(course))
    return added_course


@router.put("/{course_code}", response_model=Course)
async def update_course_data(course_code: str, req: UpdateCourse = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    if len(req) < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Update request not valid"},
        )
    updated_course = await update_course(course_code, req)

    if updated_course:
        return updated_course
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Course with id {course_code} not found",
    )
