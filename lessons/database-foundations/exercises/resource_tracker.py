"""Starter project for a community-resource tracker."""

import sqlite3


def create_table(connection: sqlite3.Connection) -> None:
    """Create the resources table."""
    # TODO: Create a table with id, name, category, and neighborhood columns.
    pass


def add_resource(
    connection: sqlite3.Connection,
    name: str,
    category: str,
    neighborhood: str,
) -> None:
    """Add one resource using SQL parameters."""
    # TODO: Insert the three values. Do not use an f-string for the SQL.
    pass


def find_resources(
    connection: sqlite3.Connection,
    category: str,
) -> list[tuple[int, str, str, str]]:
    """Return resources matching a category."""
    # TODO: Select matching records and return cursor.fetchall().
    return []


def main() -> None:
    """Create the database and provide a small test of each function."""
    with sqlite3.connect("resources.db") as connection:
        create_table(connection)

        # TODO: Add sample resources, search for one category, and print results.


if __name__ == "__main__":
    main()
