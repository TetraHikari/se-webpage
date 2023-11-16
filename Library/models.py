from pydantic import BaseModel

class Book(BaseModel):
    book_id: str
    title: str