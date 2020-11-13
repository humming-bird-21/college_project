from pydantic import BaseModel, Field
from typing import List, Optional


class Subject(BaseModel):
    name: str = Field(
        ..., min_length=4, max_length=100, description="Name for the subject"
    )
    subject_code: str = Field(
        ..., min_length=5, max_length=20, description="Unique code for the subject"
    )
    max_marks: int = Field(..., gt=0, le=100)
    min_marks: int = Field(..., gt=0, le=100)


class UpdateSubject(BaseModel):
    name: Optional[str] = Field(
        None, min_length=4, max_length=100, description="Name for the subject"
    )
    max_marks: Optional[int] = Field(None, gt=0, le=100)
    min_marks: Optional[int] = Field(None, gt=0, le=100)
