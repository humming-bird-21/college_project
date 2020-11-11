from typing import List

from fastapi import APIRouter, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from server.database import retrieve_subjects, insert_subject
from server.schemas.common import Message, RecordStatus
from server.schemas.student import Student, StudentDB, UpdateStudent
from server.schemas.subjects import Subject

router = APIRouter()


@router.get("/", response_model=List[Subject])
async def get_all_subjects():
    subjects = await retrieve_subjects()
    return subjects


@router.post("/", response_model=Subject)
async def add_subject(subject: Subject):
    added_subject = await insert_subject(jsonable_encoder(subject))
    return added_subject
