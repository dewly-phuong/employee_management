from .beanie_repository import BeanieRepository
from ..models.user import User

class UserRepository(BeanieRepository):
    def __init__(self):
        super().__init__(User)
        
user_repository = UserRepository()
