# Week 3: Programming Foundations and Engineering Output

Week 2 proved that students can use ChatGPT to turn an idea into a working app. Week 3 slows the process down and examines what makes the app work. AI can multiply an engineer's output, but the engineer remains the starting value. Stronger fundamentals help students ask better questions, recognize broken code, make deliberate changes, and build beyond the first generated draft.

The lesson contains three connected modules. Each module adds a capability to an **Engineering Output Tracker**, and the final challenge combines variables, decisions, loops, lists, and functions in one runnable program.

Guided exercises use Jupyter notebooks so students can run one concept at a time and keep explanations beside the code. The final application remains a normal Python program with `start.bat`; notebooks support learning, while the `.py` file practices delivering a runnable product.

## Beginner teaching pattern

Use the same five-step routine throughout all three modules:

1. **Read:** Identify the new line or concept together.
2. **Predict:** Students say or write what they expect before running anything.
3. **Run:** Execute one small cell with `Shift+Enter`.
4. **Change:** Modify one value or one line, then run it again.
5. **Explain:** A student describes what changed in plain language.

Do not begin with a blank cell. Model one complete example, complete the next example as a class, and then let students finish a closely related checkpoint. Stop at each **Checkpoint** marker until most students can show the expected output. Pair students who finish early with classmates who want help explaining an error; early finishers should not race several sections ahead.

## Learning objectives

By the end of class, students can:

- Trace a small Python program from input through processing to output.
- Store and update values with clearly named variables.
- Convert text input to a number and use a conditional to make a decision.
- Use a list and a loop to process several values.
- Choose between a `for` loop and a `while` loop.
- Define a function with parameters and a return value.
- Break one large problem into smaller functions.
- Explain and test code before accepting AI-generated changes.

## Saturday agenda

| Time | Block |
| --- | --- |
| 9:00-9:10 | Icebreaker: Anonymous Opinion Box |
| 9:10-9:20 | Bridge from Week 2 vibe coding |
| 9:20-9:33 | Output multiplier and objectives |
| 9:33-9:45 | Jupyter setup, weekly pull, and prediction challenge |
| 9:45-10:25 | Module 1: data, variables, input/output, and decisions |
| 10:25-10:35 | Break |
| 10:35-11:20 | Module 2: lists, `for` loops, and `while` loops |
| 11:20-11:30 | Break |
| 11:30-12:25 | Module 3: functions, decomposition, and integrated build |
| 12:25-12:45 | Peer run, code trace, and debugging |
| 12:45-1:00 | Exit ticket and engineering reflection |

## Opening bridge: output is multiplied

Start with the **Anonymous Opinion Box**, a seated, nontechnical social icebreaker. Give each student a small piece of paper. Students choose one prompt, write for 60 seconds without adding a name, fold the paper, and pass it forward. Shuffle the answers and read five or six aloud. Invite comments only when students volunteer, and do not guess who wrote an answer.

Prompts include what is actually worth the hype, what everyone should try once, and what small thing instantly improves a day. Move into the Week 2 bridge after ten minutes.

Use the informal model:

```text
engineering output = your foundation × tools × practice
```

The `100×` claim is a thought experiment, not a measured promise. Ask students to compare two situations:

- A developer copies an AI response but cannot explain or test it.
- A developer understands the inputs, data, decisions, repetition, and functions well enough to direct and verify the AI.

The tool may be identical. The second developer produces more reliable output because the value being multiplied is stronger.

Ask students to open the app they built in Week 2 and identify one example of each item they can find: input, stored data, processing, output, and repetition. Missing concepts are allowed. The goal is to expose what they can already recognize and what they will learn today.

## Key vocabulary

- **Input:** Data received by a program.
- **Output:** Information or an action produced by a program.
- **Variable:** A name that refers to a stored value.
- **Data type:** The kind of value being stored, such as `str`, `int`, `float`, or `bool`.
- **Expression:** Values and operators that Python evaluates to produce a result.
- **Conditional:** Code that chooses a path using a Boolean condition.
- **List:** An ordered collection of values.
- **Loop:** Code that repeats.
- **Iteration:** One pass through a loop.
- **Function:** A named, reusable block of code.
- **Parameter:** A name that receives a value when a function runs.
- **Return value:** A result sent back by a function.
- **Decomposition:** Breaking a problem into smaller parts.
- **Trace:** Following the program's values and control flow step by step.

## Module 1: data, variables, input/output, and decisions

Run [`examples/module_1_data_and_decisions.py`](examples/module_1_data_and_decisions.py) from the repository root:

```powershell
python week-03-programming-foundations/examples/module_1_data_and_decisions.py
```

Instructor sequence:

1. Predict the type returned by `input()`.
2. Trace values from input to variables, expressions, and printed output.
3. Show why `int()` is needed before arithmetic.
4. Change one input and predict which conditional branch will run.
5. Intentionally remove the conversion and read the resulting error.

Students complete [`exercises/module-1-data-decisions.md`](exercises/module-1-data-decisions.md).
Use [`exercises/module-1-data-decisions.ipynb`](exercises/module-1-data-decisions.ipynb) as the working notebook.

## Module 2: collections and repetition

Run [`examples/module_2_loops_and_lists.py`](examples/module_2_loops_and_lists.py).

Use `for` when processing a known collection or range. Use `while` when repetition depends on a condition that can change. Trace the loop variable and accumulator after every iteration. Discuss common infinite-loop causes before students write a `while` loop.

Students complete [`exercises/module-2-loops.md`](exercises/module-2-loops.md).
Use [`exercises/module-2-loops.ipynb`](exercises/module-2-loops.ipynb) as the working notebook.

## Module 3: functions and decomposition

Run [`examples/module_3_functions.py`](examples/module_3_functions.py).

Model the difference between printing a value and returning a value. Trace how arguments become parameters and how a return value moves back to the calling code. Refactor repeated logic into one small function before students work on the integrated challenge.

Students complete [`exercises/module-3-functions.md`](exercises/module-3-functions.md).
Use [`exercises/module-3-functions.ipynb`](exercises/module-3-functions.ipynb) as the working notebook.

## Integrated challenge: Engineering Output Tracker

Students open [`assignment/output_tracker.py`](assignment/output_tracker.py). The starter runs immediately and contains three marked tasks:

Students first prototype in [`assignment/output-tracker-workbook.ipynb`](assignment/output-tracker-workbook.ipynb), then transfer the finished functions into the runnable `.py` file.

1. Replace the placeholder calculation with a loop that processes every practice session.
2. Add a useful decision based on the calculated score.
3. Add one output that uses the scores list.

The minimum finished version must:

- Ask for the student's name.
- Collect at least three practice-session scores.
- Store the scores in a list.
- Use a loop to calculate a total or average.
- Use a conditional to give a useful message.
- Use at least two student-written functions.
- Launch by double-clicking `start.bat`.

Students may ask ChatGPT for explanations, test cases, or help with one bounded change. They must be able to trace every line they keep.

## Peer run, code trace, and debugging

Partners use [`exercises/peer-code-review.md`](exercises/peer-code-review.md):

1. Launch the app with `start.bat`.
2. Test normal, boundary, and unexpected input.
3. Choose one function and trace its arguments, parameters, and return value.
4. Identify one variable whose name makes the code easier or harder to understand.
5. Request one small improvement.

Developers repair one issue or implement one improvement, then rerun the same test that exposed the problem.

## Exit ticket

1. In the output-multiplier model, what part represents you?
2. When would you choose a `for` loop instead of a `while` loop?
3. What is the difference between `print()` and `return`?
4. Which function in your project has one clear job?
5. What can you now verify that you could not confidently verify during Week 2?

## Optional extensions

- Reject scores outside the range 0 through 10.
- Keep asking until the user enters a valid number.
- Add a function that finds the highest score without using `max()`.
- Let the user enter any number of sessions and type `done` to finish.
- Ask ChatGPT for five edge cases, then test them without requesting code.
