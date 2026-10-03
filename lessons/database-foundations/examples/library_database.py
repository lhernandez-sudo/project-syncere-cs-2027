"""Demonstrate basic SQLite operations with an in-memory database."""

import sqlite3


def create_table(connection: sqlite3.Connection) -> None:
    """Create the books table if it does not already exist."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            available INTEGER NOT NULL DEFAULT 1
        )
        """
    )


def add_book(connection: sqlite3.Connection, title: str, author: str) -> None:
    """Insert one book using safe SQL parameters."""
    connection.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author),
    )


def show_available_books(connection: sqlite3.Connection) -> None:
    """Display available books in title order."""
    rows = connection.execute(
        """
        SELECT id, title, author
        FROM books
        WHERE available = ?
        ORDER BY title
        """,
        (1,),
    )

    for book_id, title, author in rows:
        print(f"{book_id}: {title} by {author}")


def main() -> None:
    """Create, update, and query a temporary demonstration database."""
    with sqlite3.connect(":memory:") as connection:
        create_table(connection)
        add_book(connection, "Python Crash Course", "Eric Matthes")
        add_book(connection, "Automate the Boring Stuff", "Al Sweigart")

        connection.execute(
            "UPDATE books SET available = ? WHERE title = ?",
            (0, "Python Crash Course"),
        )

        print("Available books:")
        show_available_books(connection)


if __name__ == "__main__":
    main()
