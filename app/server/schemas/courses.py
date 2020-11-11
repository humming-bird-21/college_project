from pydantic import BaseModel, Field
from typing import List


class Course(BaseModel):
    name: str = Field(
        ..., min_length=3, max_length=100, description="Name for the course"
    )
    course_code: str = Field(
        ..., min_length=3, max_length=100, description="Unique Code for the Course"
    )
    mandatory_subjects: List[str] = Field(
        ...,
        description="List of subjects(codes) mandatory for the course",
    )
    optional_subjects: List[str] = Field(
        ..., description="List of subjects(codes) optional for the course"
    )
    max_optional_subjects: int = Field(
        ..., gt=0, le=10, description="Maximum of optional subjects"
    )
