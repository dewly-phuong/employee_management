from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class MongoDB:
    """docstring for MongoDB."""

    def __init__(self, db_name: str = "company_db"):
        logger.info("INITIALIZE MONGODB SESSION")
        self.client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        logger.info(f"GET COLLECTION {collection_name}")
        return self.db[collection_name]

    def close(self):
        logger.info("CLOSE MONGODB SESSION")
        self.client.close()
