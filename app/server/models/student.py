from pydantic import BaseModel, EmailStr, Field
import sys
from uuid import UUID, uuid4
from datetime import datetime, date
from typing import Optional, List
from .common import StudentStatus
from ..utils.support import History


class UpdateStudent(BaseModel):
    first_name: Optional[str] = Field(
        None,
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
    last_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Last Name for Student",
        example="Rambo",
    )
    mothers_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Mothers Name for Student",
        example="Hilary",
    )
    date_of_birth: Optional[date] = Field(
        None, description="Date of Birth for student as per ISO8601"
    )
    address: Optional[str] = Field(
        None,
        min_length=1,
        max_length=500,
        description="Communication address for student",
    )
    contant_number: Optional[str] = Field(
        None,
        regex="^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$",
    )
    email: Optional[EmailStr] = Field(
        None, description="Email address for communication with student"
    )
    status: Optional[StudentStatus] = Field(None, description="status for the student")


class Student(BaseModel):
    prn: int = Field(
        ...,
        gt=0,
        le=sys.maxsize,
        description="PRN number for the student",
        example="123456789",
    )
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


class StudentDB(Student):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    history: Optional[List[History]] = Field(
        [], description="Student Update History Series"
    )
