from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from psycopg2 import sql
from psycopg2.errors import DuplicateDatabase
import psycopg2
from models.books import Book, get_books

# Database configuration
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "admin"
DATABASE_NAME = "library_db"
SERVER_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/"
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{DATABASE_NAME}"

def create_database():
    conn = None
    try:
        conn = psycopg2.connect(SERVER_URL)
        conn.autocommit = True
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DATABASE_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE_NAME)))
            print(f"Database {DATABASE_NAME} created successfully.")
        else:
            print(f"Database {DATABASE_NAME} already exists.")
            
    except DuplicateDatabase:
        print(f"Database {DATABASE_NAME} already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        if conn is not None:
            conn.close()

def create_tables():
    create_database()
    
    try:
        engine = create_engine(DATABASE_URL)
        SQLModel.metadata.create_all(engine)  # Use SQLModel metadata
        print("Tables created successfully.")
    except OperationalError as e:
        print(f"Failed to create tables: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def insert_books():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Verify if the 'books' table exists
        inspector = inspect(engine)
        if 'books' not in inspector.get_table_names():
            print("Error: 'books' table does not exist. Please run `create_tables()` first.")
            return

        # Get existing books
        existing_books = session.query(Book.title).all()
        existing_titles = {book[0] for book in existing_books}

        # Get all books to insert
        books_to_insert = [book for book in get_books() if book.title not in existing_titles]

        if books_to_insert:
            session.add_all(books_to_insert)
            session.commit()
            print(f"Inserted {len(books_to_insert)} new books.")
        else:
            print("All books already exist in the database.")

    except Exception as e:
        session.rollback()
        print(f"Error inserting books: {e}")
    finally:
        session.close()