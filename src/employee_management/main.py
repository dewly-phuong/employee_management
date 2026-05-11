from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api.routers import users
from .database import MongoDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Perform anything startup with app here
    # Initialize mongo database client
    app.state.mongo_client = MongoDB("company_db")
    yield
    # Close Mongo database connection
    app.state.mongo_client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
