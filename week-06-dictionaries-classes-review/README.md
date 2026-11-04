# Week 6: Dictionaries and Friendly Classes Review

This is the final foundations review before students begin the December capstone. The instructor is absent, so the session is fully self-guided through Google Colab. The notebooks introduce dictionaries as a core data structure and classes as an optional way to organize related data and behavior.

## Learning objectives

By 1:00 PM, students can:

- Create, read, update, and safely access dictionary values.
- Loop through dictionary keys and values.
- Select a dictionary for one structured record or a class for many objects with shared behavior.
- Define a simple class with `__init__`, attributes, and methods.
- Create two independent objects from the same class.
- Use embedded checks to locate syntax and functionality problems.

## Google Colab launch links

Students should open each notebook, choose **File → Save a copy in Drive**, and work only in the saved copy.

1. [Icebreaker: Secret Identity Generator](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-06-dictionaries-classes-review/exercises/00-icebreaker-secret-identity.ipynb)
2. [Notebook 1: Dictionary Arcade](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-06-dictionaries-classes-review/exercises/01-dictionary-arcade.ipynb)
3. [Notebook 2: Friendly Character Classes](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-06-dictionaries-classes-review/exercises/02-friendly-character-classes.ipynb)
4. [Notebook 3: Data Model Showdown](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-06-dictionaries-classes-review/exercises/03-data-model-showdown.ipynb)

## Saturday agenda

| Time | Block |
| --- | --- |
| 9:00-9:15 | Arrival, sign-in, and open the Week 6 README |
| 9:15-9:35 | Secret Identity Generator icebreaker |
| 9:35-10:25 | Notebook 1: Dictionary Arcade |
| 10:25-10:35 | Break |
| 10:35-11:20 | Finish Dictionary Arcade and complete its boss challenge |
| 11:20-11:30 | Break |
| 11:30-12:15 | Notebook 2: Friendly Character Classes |
| 12:15-12:40 | Notebook 3: Data Model Showdown |
| 12:40-12:52 | Final self-test and repair |
| 12:52-1:00 | Exit ticket and save notebooks to Drive |

## Work style

Each student keeps an individual Colab copy and completes their own work. There are no assigned teams, roles, public votes, or required presentations.

- Try each challenge independently first.
- Predict the result before pressing Run.
- Read the failed check before changing code.
- After one repair attempt, students may quietly compare with a neighbor.
- Sharing an icebreaker identity is optional.

## Key vocabulary

- **Dictionary:** A collection of key-value pairs.
- **Key:** The label used to find a dictionary value.
- **Value:** The data stored under a key.
- **Class:** A blueprint for objects that share attributes and methods.
- **Object:** One instance created from a class.
- **Attribute:** A value stored on an object.
- **Method:** A function defined inside a class.
- **`__init__`:** The method that sets an object's starting state.
- **`self`:** The current object receiving a method call.

## Self-guided lesson sequence

There is no live lesson this week. Each notebook follows the same routine:

1. Read the concept explanation.
2. Predict the example output.
3. Run the working example.
4. Run the starter challenge once.
5. Read every failed integrity check.
6. Repair one small part at a time.
7. Rerun until every check passes.

Syntax errors must be fixed before a cell can reach its checks. Functionality checks use several inputs so a single hard-coded answer will not pass.

## Guided exercises

Notebook 1 builds a game inventory and student event record with dictionaries. Notebook 2 builds simple `Character` and `PowerUp` classes. Notebook 3 compares both approaches and produces a small player roster system.

## Challenge artifact

Each student finishes with a working roster program that stores a club profile in a dictionary and creates independent `Player` objects. The final cell prints the roster and passes all checks.

## Final self-test

At 12:40, each student runs the final challenge, creates a new test object, changes its values, and confirms that the output updates. Students leave a Markdown note naming one successful design choice and one repaired issue. A neighbor may review the result only if both students want help.

## Exit ticket

1. What problem does a dictionary solve?
2. Why might `.get()` be safer than square brackets for an optional key?
3. What is the difference between a class and an object?
4. Why should two `Player` objects keep separate scores?
5. Which structure might help your capstone: a dictionary, a class, or both? Explain.

## Optional extensions

- Add a nested dictionary for character equipment.
- Add a healing method to the `Player` class.
- Add input validation without changing the integrity checks.
- Create a second object type only if the first class is fully understood.

The editable substitute deck is in `slides/week-06-dictionaries-classes-review-v3.pptx`.
