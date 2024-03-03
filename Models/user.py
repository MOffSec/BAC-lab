from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define database connection details
DATABASE_URL = "sqlite:///Database/open.db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
# Create a base class for SQLAlchemy models
Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")


# Create database tables (if they don't already exist)
Base.metadata.create_all(bind=engine)

# Create a database session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
