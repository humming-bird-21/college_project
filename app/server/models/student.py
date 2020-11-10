from pydantic import BaseModel, EmailStr, Field, PrivateAttr, validator
from fastapi import Body
import sys
from uuid import UUID, uuid4
from datetime import datetime, date
from typing import Optional, List
from bson.objectid import ObjectId
from .common import StudentStatus


class UpdateStudent(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="First Name for Student",
        example="John",
    )
    middle_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Middle Name for Student",
        example="H",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Last Name for Student",
        example="Rambo",
    )
    mothers_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Mothers Name for Student",
        example="Hilary",
    )
    date_of_birth: date = Field(
        ..., description="Date of Birth for student as per ISO8601"
    )
    address: Optional[str] = Field(
        None,
        min_length=1,
        max_length=500,
        description="Communication address for student",
    )
    contant_number: Optional[str] = Field(
        ..., regex="^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$"
    )
    email: EmailStr = Field(
        ..., description="Email address for communication with student"
    )
    status: StudentStatus = Field(
        StudentStatus.active, description="status for the student"
    )


class Student(UpdateStudent):
    prn: int = Field(
        ...,
        gt=0,
        le=sys.maxsize,
        description="PRN number for the student",
        example="123456789",
    )


class StudentDB(Student):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
