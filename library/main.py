import uvicorn
from fastapi import FastAPI
from library.books.routers import router as router_books

app = FastAPI()

app.include_router(router_books)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)