from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel
from datetime import datetime

client = MongoClient('mongodb://localhost:27017')
db = client['se-blog']
collection = db['posts']


class Post(BaseModel):
    title: str
    content: str
    created_at: datetime = datetime.now()
    
    def created_at_readable(self):
        return self.created_at.strftime("%B %d, %Y, %I:%M %p")
    
