from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, complaints

app = FastAPI()

app.include_router(users.router)
app.include_router(complaints.router)

models.Base.metadata.create_all(bind=engine)






