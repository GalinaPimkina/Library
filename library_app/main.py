import uvicorn
from fastapi import FastAPI
from routers.books import router as router_books
from routers.students import router as router_students
from routers.auth import router as auth_router

app = FastAPI()

app.include_router(router_books)
app.include_router(router_students)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)