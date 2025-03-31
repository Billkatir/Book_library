from models.db_init import create_tables, insert_books

def main():
    # Initialize the database and create tables if they don't exist
    create_tables()
    insert_books()
    print("Database initialized and tables created.")

if __name__ == "__main__":
    main()