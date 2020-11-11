from datetime import datetime

import motor.motor_asyncio
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from server.schemas.common import RecordStatus
from server.schemas.student import StudentDB
from server.utils.support import History

MONGO_DETAILS = "mongodb://root:example@localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.college

student_collection = database.get_collection("students")
subject_collection = database.get_collection("subjects")
course_collection = database.get_collection("course")

# Retrieve all students present in the database
async def retrieve_students(status: RecordStatus):
    students = []
    async for student in student_collection.find({"record": status}):
        students.append(student)
    return students


async def find_student_by_first_last_name(student: dict):
    student_from_db = await student_collection.find_one(
        {
            "first_name": student["first_name"],
            "last_name": student["last_name"],
            "middle_name": student["middle_name"],
        }
    )
    if student_from_db:
        return student_from_db
    return False


async def find_student_by_prn(student: dict):
    student_from_db = await student_collection.find_one(
        {"prn": student["prn"]},
    )
    if student_from_db:
        return student_from_db
    return False


# Add a new student into to the database
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one(
        {"_id": ObjectId(student.inserted_id)}
    )
    return new_student


# Retrieve a student with a matching ID
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"id": id})
    if student:
        return student


# Update a student with a matching ID
async def update_student(id: str, data: dict):
    # Return false if an empty request body is sent.
    student = await student_collection.find_one({"id": id})

    if student:
        for k, v in data.items():
            student[k] = v
        student["timestamp"] = datetime.utcnow()
        student["history"].append(History(update_data=data))
        updated_student = await student_collection.update_one(
            {"id": id}, {"$set": jsonable_encoder(StudentDB(**student))}
        )
        if updated_student:
            return await student_collection.find_one({"id": id})
        return None


# Delete a student from the database
async def delete_student(id: str):
    student = await student_collection.find_one(
        {"id": id, "record": RecordStatus.active}
    )
    if student:
        result = await student_collection.update_one(
            {"id": id}, {"$set": {"record": RecordStatus.deleted}}
        )
        return result
    return False


async def retrieve_subjects():
    subjects = []
    async for subject in subject_collection.find():
        subjects.append(subject)
    return subjects


async def insert_subject(subject: dict):
    subject = await subject_collection.insert_one(subject)
    new_subject = await subject_collection.find_one(
        {"_id": ObjectId(subject.inserted_id)}
    )
    return new_subject


async def retrieve_courses():
    courses = []
    async for course in course_collection.find():
        courses.append(course)
    return courses


async def insert_course(course: dict):
    course_db = await course_collection.insert_one(course)
    new_course = await course_collection.find_one(
        {"_id": ObjectId(course_db.inserted_id)}
    )
    return new_course
