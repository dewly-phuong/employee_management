from .beanie_repository import BeanieRepository
from ..models.project import Project

class ProjectRepository(BeanieRepository):
    def __init__(self):
        super().__init__(Project)
