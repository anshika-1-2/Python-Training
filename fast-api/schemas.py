from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    year: int 
    
    
class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None

class Book(BookBase):
    
    id: int
    
    class Config:
        # orm_mode = True
        from_attributes = True
        
