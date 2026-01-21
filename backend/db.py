from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import models

# This creates a local SQLite database file named "vigil_ai.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./vigil_ai.db"

# Create the engine
# "check_same_thread" is only needed for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class (each instance is a database session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models to inherit from
Base = declarative_base()

# Dependency to get the database session in your routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()