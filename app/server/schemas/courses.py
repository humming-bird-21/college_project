from pydantic import BaseModel, Field
from typing import List, Optional


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


class UpdateCourse(BaseModel):
    name: Optional[str] = Field(
        None, min_length=3, max_length=100, description="Name for the course"
    )
    mandatory_subjects: Optional[List[str]] = Field(
        None,
        description="List of subjects(codes) for the course",
    )
    optional_subjects: Optional[List[str]] = Field(
        None, description="List of subjects(codes) optional for the course"
    )
    max_optional_subjects: Optional[int] = Field(
        None, gt=0, le=10, description="Maximum of optional subjects"
    )
