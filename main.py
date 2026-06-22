from fastapi import FastAPI

from admin import setup_admin
from database import Base, engine
from routes.board import router as board_router
from routes.task import router as task_router
from routes.user import router as user_router

Base.metadata.create_all(bind=engine)

# Simplified task board-like API
app = FastAPI()

app.include_router(board_router)
app.include_router(task_router)
app.include_router(user_router)

setup_admin(app)
