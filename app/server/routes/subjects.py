from typing import List

from fastapi import APIRouter, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from server.database import retrieve_subjects, insert_subject, subject_collection
from server.schemas.common import Message, RecordStatus, ResponseException
from server.schemas.student import Student, StudentDB, UpdateStudent
from server.schemas.subjects import Subject

router = APIRouter()


async def precondition_subject_by_code(subject: dict):
    subject_from_db = await subject_collection.find_one(
        {"subject_code": subject["subject_code"]}
    )
    if subject_from_db:
        raise HTTPException(
            status_code=412,
            detail=f"Student with same Subject Code ({subject_from_db['subject_code']}) already present",
        )
    return False


@router.get("/", response_model=List[Subject])
async def get_all_subjects():
    subjects = await retrieve_subjects()
    return subjects


@router.post(
    "/",
    response_model=Subject,
    responses={status.HTTP_412_PRECONDITION_FAILED: {"model": ResponseException}},
)
async def add_subject(subject: Subject):
    await precondition_subject_by_code(jsonable_encoder(subject))
    added_subject = await insert_subject(jsonable_encoder(subject))
    return added_subject
