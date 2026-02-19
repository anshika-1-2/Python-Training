from fastapi import FastAPI, Depends, HTTPException
import services, models, schemas

from db import get_db, create_table
from sqlalchemy.orm import Session 
app = FastAPI()

@app.get("/books", response_model=list[schemas.Book])

def get_all_books(db: Session = Depends(get_db)):
    """Get all books in the database
    
    Returns:
        List[schemas.Book]: A list of all books in the database
    """
    return services.get_books(db)

@app.post("/books", response_model=schemas.Book)

def create_new_book(data: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book in the database
    
    Args:
        data (schemas.BookCreate): The book data to be created
        db (Session): The database session

    Returns:
        schemas.Book: The created book
    """
    return services.BookCreate(db, data)


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """Get a book by its ID

    Args:
        book_id (int): The ID of the book
        db (Session): The database session

    Returns:
        schemas.Book: The book with the given ID

    Raises:
        HTTPException: If the book is not found
    """
    book_queryset = services.get_book(db, book_id)
    if not book_queryset:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_queryset


@app.put("/books/{book_id}", response_model=schemas.Book)

def update_book(book_id: int, data: schemas.BookCreate, db: Session = Depends(get_db)):
    """Update a book in the database
    
    Args:
        book_id (int): The ID of the book to update
        data (schemas.BookCreate): The book data to be updated
        db (Session): The database session

    Returns:
        schemas.Book: The updated book

    Raises:
        HTTPException: If the book is not found
    """
    db_update= services.update_book(db, book_id, data)
    if not db_update:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_update

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book from the database by its ID

    Args:
        book_id (int): The ID of the book to delete
        db (Session): The database session

    Returns:
        schemas.Book: The deleted book

    Raises:
        HTTPException: If the book is not found
    """
    delete_entry = services.delete_book(db, book_id)
    if not delete_entry:
        raise HTTPException(status_code=404, detail="Book not found")   
    return delete_entry



@app.patch("/books/{book_id}", response_model=schemas.Book)
def partial_update_book(book_id: int,data: schemas.BookUpdate,db: Session = Depends(get_db)):
    """
    Partially update a book by its ID

    Args:
        book_id (int): The ID of the book to update
        data (schemas.BookUpdate): The book data to be updated
        db (Session): The database session

    Returns:
        schemas.Book: The updated book

    Raises:
        HTTPException: If the book is not found
    """
    updated_book = services.patch_book(db, book_id, data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book
