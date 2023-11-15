from pydantic import BaseModel

class Room(BaseModel):
    username: str
    email: str