from database import Base, engine
from fastapi import FastAPI
from routes.boards import router as boards_router
from routes.tasks import router as tasks_router
from routes.users import router as users_router

Base.metadata.create_all(bind=engine)

# Simplified task board-like API
app = FastAPI()


app.include_router(boards_router)
app.include_router(tasks_router)
app.include_router(users_router)
