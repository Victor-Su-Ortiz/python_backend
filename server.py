from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.database import Base, engine
from app.core.config import settings
from app.routes import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management App")

app.add_middleware(CORSMiddleware)

app.include_router(tasks.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def read_root():
    return {"Message": f"Welcome to the {settings.APP_NAME}"}
