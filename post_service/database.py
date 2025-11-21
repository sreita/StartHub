from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your actual database URL
# For example: "postgresql://user:password@host:port/database"
# We will use a local SQLite database for initial development.
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, 
    # The connect_args are only needed for SQLite
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency to get a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
