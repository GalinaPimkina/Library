import uvicorn
from fastapi import FastAPI
from api import router as router_v1

app = FastAPI()

app.include_router(router=router_v1)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)