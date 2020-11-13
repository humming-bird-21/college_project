from fastapi import FastAPI
from .routes.student import router as StudentRouter
from .routes.subject import router as SubjectsRouter
from .routes.courses import router as CoursesRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")
app.include_router(SubjectsRouter, tags=["Subject"], prefix="/subject")
app.include_router(CoursesRouter, tags=["Course"], prefix="/course")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
