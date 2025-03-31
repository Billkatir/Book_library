const express = require('express');
const { Pool } = require('pg');
const path = require('path'); // For handling file paths

const app = express();
const PORT = 3000;

// PostgreSQL connection configuration
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'library_db',
  password: 'admin',
  port: 5432,
});

// Middleware to parse JSON
app.use(express.json());

// Serve static files (e.g., index.html, CSS, JS)
app.use(express.static(path.join(__dirname, 'public')));

// Route to serve the main HTML file when accessing the root URL
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API Routes

// Get all book IDs
app.get('/books/ids', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM books ORDER BY id');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

// Get all unique authors
app.get('/books/authors', async (req, res) => {
  try {
    const result = await pool.query('SELECT DISTINCT author FROM books ORDER BY author');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

// Get a specific book by ID
app.get('/books/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query('SELECT * FROM books WHERE id = $1', [id]);
    if (result.rows.length > 0) {
      res.json(result.rows[0]);
    } else {
      res.status(404).send('Book not found');
    }
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

// Get all books by a specific author
app.get('/books/author/:author', async (req, res) => {
  const { author } = req.params;
  try {
    const result = await pool.query('SELECT * FROM books WHERE author = $1', [author]);
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

// Get all books available for borrowing
app.get('/books/available/borrow', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM books WHERE available_borrow = TRUE');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

// Get all books available for purchase
app.get('/books/available/buy', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM books WHERE available_buy = TRUE');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

// Borrow a book
app.post('/book/borrow/id/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query(
      'UPDATE books SET available_borrow = FALSE,available_buy = FALSE WHERE id = $1 AND available_borrow = TRUE RETURNING *',
      [id]
    );
    console.log('Query Result:', result);
    if (result.rowCount > 0) {
      res.json({
        message: 'Book borrowed successfully',
        book: result.rows[0],
      });
    } else {
      res.status(201).json({
        message: 'Book is not available for borrowing or does not exist',
      });
    }
  } catch (err) {
    console.error('Error during borrow operation:', err);
    res.status(500).json({
      message: 'Server error',
    });
  }
});

// Buy a book
app.post('/book/buy/id/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query(
      'UPDATE books SET available_buy = FALSE, available_borrow = FALSE WHERE id = $1 AND available_buy = TRUE RETURNING *',
      [id]
    );
    console.log('Query Result:', result);
    if (result.rowCount > 0) {
      res.json({
        message: 'Book purchased successfully',
        book: result.rows[0],
      });
    } else {
      res.status(201).json({
        message: 'Book is not available for purchase or does not exist',
      });
    }
  } catch (err) {
    console.error('Error during purchase operation:', err);
    res.status(500).json({
      message: 'Server error',
    });
  }
});

// Return a borrowed book
app.post('/book/return/id/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query(
      'UPDATE books SET available_borrow = TRUE, available_buy= TRUE  WHERE id = $1 AND available_borrow = FALSE AND available_buy = FALSE RETURNING *',
      [id]
    );
    console.log('Query Result:', result);
    if (result.rowCount > 0) {
      res.json({
        message: 'Book returned successfully',
        book: result.rows[0],
      });
    } else {
      res.status(201).json({
        message: 'Book does not exist or was not borrowed',
      });
    }
  } catch (err) {
    console.error('Error during returning operation:', err);
    res.status(500).json({
      message: 'Server error',
    });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});