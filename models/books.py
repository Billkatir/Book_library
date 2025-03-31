from sqlmodel import Field, SQLModel
from typing import List

class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: int = Field(default=None, primary_key=True)
    title: str
    author: str
    available: bool = Field(default=True)

def get_books() -> List[Book]:
    books = []
    authors = [f"auth_{i+1}" for i in range(4)]  # Create 4 authors
    
    for i in range(1, 21):  # Create 20 books
        book = Book(
            title=f"title_{i}",
            author=authors[i % 4],  # Cycle through the 4 authors
            available=True
        )
        books.append(book)
    
    return books