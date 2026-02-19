from models import Book 
from sqlalchemy.orm import Session
from schemas import BookCreate
from schemas import BookUpdate

def BookCreate(db: Session, data: BookCreate):
    """
    Create a new book in the database.

    Args:
        db (Session): The SQLAlchemy session to use.
        data (BookCreate): The data to use when creating the new book.

    Returns:
        Book: The newly created book.
    """
    book_instance = Book(**data.model_dump())
    db.add(book_instance)
    db.commit()
    db.refresh(book_instance)
    return book_instance 


def get_books(db: Session):
    """
    Retrieve all books from the database.

    Args:
        db (Session): The SQLAlchemy session to use.

    Returns:
        List[Book]: A list of all books in the database.
    """
    return db.query(Book).all()


def get_book(db: Session, book_id: int):
    """
    Retrieve a book from the database by its ID.

    Args:
        db (Session): The SQLAlchemy session to use.
        book_id (int): The ID of the book to retrieve.

    Returns:
        Book | None: The book with the given ID if it exists, otherwise None.
    """
    return db.query(Book).filter(Book.id == book_id).first()



def update_book(db: Session, book_id: int, data: BookCreate):
    """
    Update a book in the database by its ID.

    Args:
        db (Session): The SQLAlchemy session to use.
        book_id (int): The ID of the book to update.
        data (BookCreate): The data to use when updating the book.

    Returns:
        Book | None: The updated book if it exists, otherwise None.
    """
    book_queryset = db.query(Book).filter(Book.id == book_id).first()
    if book_queryset:
        for key, value in data.model_dump().items():
            setattr(book_queryset, key, value)
        db.commit()
        db.refresh(book_queryset)
    return book_queryset

def patch_book(db: Session, book_id: int, data: BookUpdate):
    """
    Partially update a book in the database by its ID.

    Args:
        db (Session): The SQLAlchemy session to use.
        book_id (int): The ID of the book to update.
        data (BookUpdate): The data to use when updating the book.

    Returns:
        Book | None: The updated book if it exists, otherwise None.
    """
    book_queryset = db.query(Book).filter(Book.id == book_id).first()

    if not book_queryset:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(book_queryset, key, value)

    db.commit()
    db.refresh(book_queryset)
    return book_queryset




def delete_book(db: Session, book_id: int):
    """
    Delete a book from the database by its ID.

    Args:
        db (Session): The SQLAlchemy session to use.
        book_id (int): The ID of the book to delete.

    Returns:
        Book | None: The deleted book if it exists, otherwise None.
    """
    book_queryset = db.query(Book).filter(Book.id == book_id).first()
    if book_queryset:
        db.delete(book_queryset)
        db.commit()
    return book_queryset


