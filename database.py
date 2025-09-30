# from sqlalchemy import create_engine, Column, Integer, String, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker
# from datetime import datetime, timezone

# Base = declarative_base()

# class FileLog(Base):
#     __tablename__ = "file_logs"
#     id = Column(Integer, primary_key=True)
#     filename = Column(String)
#     src = Column(String)
#     dest = Column(String)
#     category = Column(String)
#     moved_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# def init_db(db_path: str):
#     engine = create_engine(f"sqlite:///{db_path}")
#     Base.metadata.create_all(engine)
#     return sessionmaker(bind=engine)


from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

# Base class for SQLAlchemy ORM models
Base = declarative_base()

# ORM model for storing information about moved files
class FileLog(Base):
    # Name of the table in the database
    __tablename__ = "file_logs"
    
    # Primary key ID for each log entry
    id = Column(Integer, primary_key=True)
    # Name of the file
    filename = Column(String)
    # Source path of the file
    src = Column(String)
    # Destination path of the file
    dest = Column(String)
    # Category of the file (e.g., Images, Music)
    category = Column(String)
    # Timestamp when the file was moved, default to current UTC time
    moved_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Function to initialize the SQLite database and return a session factory
def init_db(db_path: str):
    # Create a SQLite engine using the given database path
    engine = create_engine(f"sqlite:///{db_path}")
    # Create all tables defined by ORM models
    Base.metadata.create_all(engine)
    # Return a sessionmaker bound to the engine for database interactions
    return sessionmaker(bind=engine)
