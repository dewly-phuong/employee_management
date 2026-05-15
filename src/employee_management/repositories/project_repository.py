from .beanie_repository import BeanieRepository
from ..models.project import Project

class UserRepository(BeanieRepository):
    def __init__(self):
        super().__init__(Project)
        
project_repository = UserRepository()
