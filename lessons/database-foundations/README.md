# Database Foundations with SQLite

## Where this lesson fits

Teach this lesson during the software-development phase after students are comfortable with functions, dictionaries, files, and exceptions. It works especially well immediately before APIs, or after APIs when students need to save retrieved data.

SQLite is included with Python through the `sqlite3` module, so students do not need to install a database server.

## Learning objectives

By the end of class, students should be able to:

- Explain the roles of tables, rows, columns, and primary keys.
- Create a SQLite database and table from Python.
- Use `INSERT`, `SELECT`, `UPDATE`, and `DELETE` operations.
- Filter and sort query results.
- Use SQL parameters instead of building queries with user input.
- Explain when a database is more useful than a list, dictionary, or CSV file.

## Four-hour Saturday plan

| Time | Activity |
| --- | --- |
| 9:00-9:20 | Do-now: organize a messy set of records into rows and columns |
| 9:20-9:40 | Review dictionaries and files; introduce tables and primary keys |
| 9:40-10:25 | Live coding: connect, create a table, insert rows, and select data |
| 10:25-10:35 | Break |
| 10:35-11:20 | Guided lab using [`examples/library_database.py`](examples/library_database.py) |
| 11:20-11:30 | Break |
| 11:30-12:25 | Build a community-resource tracker from the [starter](exercises/resource_tracker.py) |
| 12:25-12:45 | Peer test queries and review one database design decision |
| 12:45-1:00 | Exit ticket: choose between a list, CSV, and database for three scenarios |

## Core vocabulary

- **Database:** An organized collection of information.
- **Table:** Related information arranged in rows and columns.
- **Row:** One record, such as one book or community resource.
- **Column:** One attribute shared by records, such as a title or category.
- **Primary key:** A value that uniquely identifies a row.
- **Query:** A request to read or change information.
- **Schema:** The structure and rules of a database.

## SQL operations

The four common data operations are sometimes called CRUD:

| Operation | SQL | Purpose |
| --- | --- | --- |
| Create | `INSERT` | Add a record |
| Read | `SELECT` | Retrieve records |
| Update | `UPDATE` | Change a record |
| Delete | `DELETE` | Remove a record |

Creating the table itself uses `CREATE TABLE`:

```sql
CREATE TABLE IF NOT EXISTS resources (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    neighborhood TEXT NOT NULL
);
```

## Safe queries

Never place user input directly inside an SQL string:

```python
# Unsafe: do not teach students to build queries this way.
query = f"SELECT * FROM resources WHERE category = '{category}'"
```

Use a placeholder and pass values separately:

```python
cursor.execute(
    "SELECT * FROM resources WHERE category = ?",
    (category,),
)
```

Parameters prevent quotation-mark bugs and SQL injection. They are required for all student projects.

## Project challenge

Complete `exercises/resource_tracker.py` so a user can:

1. Add a community resource.
2. List all resources.
3. Search by category or neighborhood.
4. Update one resource.
5. Delete one resource after confirmation.

### Extension ideas

- Prevent duplicate resources.
- Add an `hours` or `website` column.
- Import initial records from a CSV file.
- Save public API results and record when they were retrieved.
- Write tests using a temporary in-memory database.

## Reflection questions

1. What problem does the primary key solve?
2. Why is a database better than a CSV file when records change frequently?
3. What could go wrong if a program inserts user input directly into SQL?
4. Which information should not be placed in a class database?

## Privacy reminder

Use fictional or public information for class projects. Do not collect passwords, private contact information, medical information, or other sensitive personal data.
