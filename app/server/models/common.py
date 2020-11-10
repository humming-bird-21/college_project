from pydantic import BaseModel
from typing import List
from enum import Enum


class ResponseModel(BaseModel):
    data: List
    code: int
    message: str


class Message(BaseModel):
    message: str


class StudentStatus(str, Enum):
    active = "active"
    dormant = "dormant"
    completed = "completed"
