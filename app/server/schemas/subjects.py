from pydantic import BaseModel, Field


class Subject(BaseModel):
    name: str = Field(
        ..., min_length=4, max_length=100, description="Name for the subject"
    )
    subject_code: str = Field(
        ..., min_length=5, max_length=20, description="Unique code for the subject"
    )
    max_marks: int = Field(..., gt=0, le=100)
    min_marks: int = Field(..., gt=0, le=100)
