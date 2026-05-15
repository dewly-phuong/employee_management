from pymongo import AsyncMongoClient
from beanie import init_beanie
from ..models.user import User
from ..models.project import Project
import logging
from ..core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        logger.info("INITIALIZE MONGODB SESSION")
        self.client: AsyncMongoClient = None
        
    async def connect(self):
        self.client = AsyncMongoClient(settings.MONGODB_URL)

        # Khởi tạo Beanie với danh sách các Document Models
        await init_beanie(
            database=self.client[settings.MONGODB_DBNAME],
            document_models=[
                User, 
                Project,
                # Thêm các class Document khác vào danh sách này khi dự án phát triển
            ],
        )
        
    def close(self):
        logger.info("CLOSE MONGODB SESSION")
        if self.client:
            self.client.close()
            
db_manger = MongoDB()

            



    
    