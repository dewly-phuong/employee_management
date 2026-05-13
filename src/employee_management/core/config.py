from fastapi.security import OAuth2PasswordBearer
from ..database import MongoDB
from pwdlib import PasswordHash

# Global instances
mongo_db = MongoDB("company_db")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hasher = PasswordHash.recommended()
