from fastapi import Request
from ..database import MongoDB

async def get_mongo_manager(request: Request):
    mongo = request.app.state.mongo_client
    return mongo