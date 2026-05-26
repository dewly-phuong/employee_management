# pyrefly: ignore [missing-import]
from pymongo import AsyncMongoClient
# pyrefly: ignore [missing-import]
from beanie import init_beanie
import logging
from uuid import uuid4
from ..models.user import User
from ..models.project import Project
from .config import get_settings
from ..services.authentication_service import password_hasher
from ..utils.enums import UserRole

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        logger.info("INITIALIZE MONGODB SESSION")
        self.client: AsyncMongoClient | None = None
        
    async def connect(self):
        logger.info("CONNECTING TO MONGODB...")
        
        settings = get_settings()
        self.client = AsyncMongoClient(settings.MONGODB_URL)
        
        
        self.db = self.client[settings.MONGODB_DBNAME]

        # Khởi tạo Beanie với danh sách các Document Models
        await init_beanie(
            database=self.db,
            document_models=[
                User, 
                Project,
                # Thêm các class Document khác vào danh sách này khi dự án phát triển
            ],
        )
        logger.info("CONNECTED TO MONGODB")
        
        users_collection = self.db["users"]
        num_users = await users_collection.count_documents({})
        if num_users == 0:
            logger.info("DATABASE IS EMPTY!")
            logger.info("INITIALIZING ROOT USER ACCOUT...")
            user = User(
                username="root",
                password=password_hasher.hash("root"),
                role=UserRole.ADMIN,
                full_name="root",
                department="root"
            )
            await user.insert()
            logger.info("ROOT USER ACCOUT INITIALIZED...")

        
    def close(self):
        logger.info("CLOSE MONGODB SESSION")
        if self.client:
            self.client.close()
            
db_manager = MongoDB()
