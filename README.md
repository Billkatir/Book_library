# 📚 Library Management System (Python + Node.js + PostgreSQL)

This project is a simple **Library Management System** that integrates:

- 🐍 Python (for database initialization and data insertion)
- 🌐 Node.js + Express (for building the RESTful API)
- 🐘 PostgreSQL (as the backend database)

It allows users to:
- View all books and authors
- Borrow, buy, or return books via API
- Serve a basic frontend from the `public` folder

---

## 📁 Project Structure

```
├── models/
│   ├── books.py            # SQLModel class for Book and sample data generation
│   └── db_init.py          # Handles database creation, table setup, and book insertion
├── public/
│   └── index.html          # Basic frontend (served by Express)
├── server.js               # Node.js + Express server (REST API)
├── main.py                 # Entry point: initializes DB and launches server
├── requirements.txt        # Python dependencies
└── README.md               # You're here!
```

---

## 🚀 Getting Started

### 1. Install Dependencies

#### 🐘 PostgreSQL
Make sure PostgreSQL is installed and running on default port `5432`.

Create a user with:
- Username: `postgres`
- Password: `admin`

> You can change these in `models/db_init.py`.

#### 🐍 Python (3.8+)
Install Python requirements:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
sqlmodel
psycopg2
sqlalchemy
```

#### 🌐 Node.js

Ensure Node.js is installed. Install Express:

```bash
npm install express pg
```

---

## ⚙️ Running the Project

### Step 1: Start Everything via Python

```bash
python main.py
```

- This will:
  - Create the PostgreSQL database `library_db`
  - Create the `books` table
  - Insert sample books (20 books across 4 authors)
  - Start the Node.js server (`server.js`)

---

## 📡 API Endpoints (Hosted at `http://localhost:3000`)

### 🧾 Books

| Method | Endpoint                      | Description                              |
|--------|-------------------------------|------------------------------------------|
| GET    | `/books/ids`                  | Get all books                            |
| GET    | `/books/authors`              | Get all unique authors                   |
| GET    | `/books/:id`                  | Get book by ID                           |
| GET    | `/books/author/:author`       | Get books by author                      |
| GET    | `/books/available/borrow`     | Get all books available to borrow        |
| GET    | `/books/available/buy`        | Get all books available to buy           |

### 📦 Actions

| Method | Endpoint                    | Description                      |
|--------|-----------------------------|----------------------------------|
| POST   | `/book/borrow/id/:id`       | Borrow a book                    |
| POST   | `/book/buy/id/:id`          | Buy a book                       |
| POST   | `/book/return/id/:id`       | Return a borrowed or bought book|

---

## 🧪 Sample Data

20 books are generated with titles like `title_1`, `title_2`, ... and authors like `auth_1`, `auth_2`, `auth_3`, `auth_4`.

---

## 📌 Notes

- Python handles all setup and database population.
- Node.js handles client-server interaction (API layer).
- Press `Ctrl+C` to gracefully stop the Node.js server.

---

## 📷 Frontend

Any files inside the `public/` folder will be statically served by Express at the root URL (`http://localhost:3000/`).

---

## 🛠️ Troubleshooting

- **PostgreSQL not found?** Make sure it's running and configured properly.
- **Node.js command not found?** Add it to your system PATH.
- **Port 3000 in use?** Modify `PORT` in `server.js`.


