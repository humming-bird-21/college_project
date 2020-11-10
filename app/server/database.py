import motor.motor_asyncio
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from server.models.student import StudentDB, History
from datetime import datetime

MONGO_DETAILS = "mongodb://root:example@localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }


# Retrieve all students present in the database
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student)
    return students


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
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
