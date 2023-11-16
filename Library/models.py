from persistent import Persistent
from pydantic import BaseModel

class BookCreate(BaseModel):
    book_id: str
    title: str
    author: str
    year: int
    genre: str
    isbn: str
    url: str

