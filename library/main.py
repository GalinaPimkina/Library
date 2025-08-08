import uvicorn
from fastapi import FastAPI
from library.routers.books import router as router_books
from library.routers.students import router as router_students

app = FastAPI()

app.include_router(router_books)
app.include_router(router_students)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)