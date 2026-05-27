from abc import ABC, abstractmethod
from uuid import UUID
from typing import Type, Mapping, Any
from pydantic import BaseModel

class IRepository(ABC):
    @abstractmethod
    async def create(self, create_request: Type[BaseModel]): pass
    @abstractmethod
    async def get_by_id(self, id: UUID): pass
    @abstractmethod
    async def get_all(self): pass
    @abstractmethod
    async def update_by_id(self, id:UUID, update_request: Type[BaseModel] | Mapping[str, Any]): pass
    @abstractmethod
    async def delete_by_id(self, id: UUID): pass
    
