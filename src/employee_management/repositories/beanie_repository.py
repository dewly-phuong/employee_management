from typing import Mapping, Type, Any
from beanie import Document, PydanticObjectId
from beanie.exceptions import DocumentNotFound
from pydantic import BaseModel
from uuid import UUID
from datetime import timezone, datetime
from .irepository import IRepository

class BeanieRepository(IRepository):
    def __init__(self, model: Type[Document]):
        self.model = model
    
    async def create(self, obj: Type[Document]):
        return await obj.insert()
    
    async def get_by_id(self, id: UUID):
        return await self.model.get(id)
    
    async def get_all(self):
        return await self.model.find_all().to_list()
    
    async def update_by_id(self, id:UUID, update_request: Type[BaseModel] | Mapping[str, Any]):
        db_object = await self.model.get(id)
        if not db_object:
            raise (ValueError, DocumentNotFound)
        if isinstance(update_request, dict):
            update_data = update_request
        else:
            update_data = update_request.model_dump(exclude_unset=True)
            
        for field in update_data:
            if hasattr(db_object, field) and (update_data[field] is not None):
                setattr(db_object, field, update_data[field])

        setattr(db_object, "updated_at", datetime.now(timezone.utc))
        await db_object.save()
        return db_object
    
    async def delete_by_id(self, id: PydanticObjectId):
        db_object = await self.model.get(id)
        if not db_object:
            raise (ValueError, DocumentNotFound)
        else:
            await db_object.delete()