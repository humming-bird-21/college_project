from fastapi import FastAPI
from .routes.student import router as StudentRouter
from .routes.subjects import router as SubjectsRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")
app.include_router(SubjectsRouter, tags=["Courses"], prefix="/subject")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
