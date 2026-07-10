from fastapi import FastAPI

from admin import setup_admin
from database import Base, engine
from routes.auth import router as auth_router
from routes.boards import router as board_router
from routes.users import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(board_router)
app.include_router(user_router)
app.include_router(auth_router)

setup_admin(app)
