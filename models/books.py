from sqlmodel import Field, SQLModel
from typing import List

class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: int = Field(default=None, primary_key=True)
    title: str
    author: str
    available_borrow: bool = Field(default=True)
    available_buy: bool = Field(default=True)
    price: int 

def get_books() -> List[Book]:
    books = []
    authors = [f"auth_{i+1}" for i in range(4)] 
    
    for i in range(1, 21):  
        book = Book(
            title=f"title_{i}",
            author=authors[i % 4],  
            available_borrow = True,
            available_buy = True,
            price = (12345 % i) + 5
        )
        books.append(book)
    
    return books    