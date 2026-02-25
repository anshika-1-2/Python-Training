from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:anshi@localhost:5432/bookstore"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db( ):
    """Yield a database session.

    The session is properly closed after it is used, even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
        
def create_table():
    """Create all tables in the database.

    This function will create all tables defined in the Base object.
    """
    Base.metadata.create_all(bind=engine)   
    