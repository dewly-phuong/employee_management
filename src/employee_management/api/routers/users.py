from fastapi import APIRouter, Depends

from ...schemas.user import User

router = APIRouter()


# @router.post("/users/")
# async def create_user(user: User, mongo: MongoDB = Depends(get_mongo_manager)):
#     employee_collection = mongo.get_collection("employees")
#     new_user = await employee_collection.insert_one(user.model_dump())
#     return {"id": str(new_user.inserted_id), "message": "User created successfully!"}
