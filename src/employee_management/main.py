from fastapi import FastAPI
from .api.routers import users, auth, projects
from .core.database import db_manger
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Perform anything startup with app here
    # Initialize mongo database client
    await db_manger.connect()
    yield
    # Close Mongo database connection
    db_manger.close()

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(projects.router)
