from fastapi import FastAPI
from .api.routers import users, auth
from .database import MongoDB
from contextlib import asynccontextmanager

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     ## Perform anything startup with app here
#     # Initialize mongo database client
#     app.state.mongo_client = await MongoDB("company_db").beanie_init()
#     yield
#     # Close Mongo database connection
#     app.state.mongo_client.close()


app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
