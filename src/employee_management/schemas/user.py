from pydantic import BaseModel


class User(BaseModel):
    username: str
    company: str
    password: str
