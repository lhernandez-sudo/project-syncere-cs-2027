# Week 1 — Python Basics

## Learning objectives

By the end of this lesson, you should be able to:

- Run a Python program from the terminal.
- Display text and values with `print()`.
- Add comments that explain code.
- Recognize a Python error message and locate the relevant line.
- Make and commit a small change with Git.

## Key ideas

A program is a set of instructions that a computer follows. Python normally runs those instructions from top to bottom.

```python
print("First instruction")
print("Second instruction")
```

Text inside quotation marks is called a string. `print()` displays a value in the terminal.

Comments begin with `#`. Python ignores comments when it runs the program:

```python
# Explain why the code exists, not merely what it says.
print("Hello!")
```

## Class activities

1. Run [`examples/hello.py`](examples/hello.py).
2. Complete [`exercises/exercises.py`](exercises/exercises.py).
3. Compare output and help a classmate diagnose one error.
4. Complete the [Week 1 assignment](assignment/README.md).

## Saturday plan

| Time | Activity |
| --- | --- |
| 9:00-9:30 | Administrative tasks: attendance, forms, accounts, and device distribution |
| 9:30-9:50 | Community introductions, course overview, and learning objectives |
| 9:50-10:25 | What computer science is, input-process-output, and the first Python program |
| 10:25-10:35 | Break |
| 10:35-11:20 | Guided lab: run, change, and debug `hello.py` |
| 11:20-11:30 | Break |
| 11:30-12:20 | Student introduction program and peer testing |
| 12:20-12:40 | Share programs and discuss one debugging discovery |
| 12:40-1:00 | Exit ticket, setup check, and reflection |

## Running Python files

From the repository root:

```bash
python week-01-python-basics/examples/hello.py
```

## Further practice

- Change every displayed message in the example.
- Intentionally remove a quotation mark, run the program, and inspect the error.
- Restore the quotation mark and confirm the program works again.
