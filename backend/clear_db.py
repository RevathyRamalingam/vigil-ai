import os
import sys

# Add the current directory to sys.path so we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine
from db import models

def clear_database():
    print(f"Connecting to database: {engine.url}")
    confirm = input("This will DELETE ALL DATA in the database. Type 'yes' to proceed: ")
    
    if confirm.lower() == 'yes':
        try:
            # Drop all tables
            models.Base.metadata.drop_all(bind=engine)
            # Recreate all tables (empty)
            models.Base.metadata.create_all(bind=engine)
            print("All tables cleared and recreated successfully!")
        except Exception as e:
            print(f"Error clearing database: {e}")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    clear_database()
