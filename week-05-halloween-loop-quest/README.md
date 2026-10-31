# Week 5 Icebreaker: Super Mario Haunted Python Kingdom

This unofficial, fan-made Super Mario Halloween side-scroller reviews the Week 3 and Week 4 Python foundations. It plays like a classroom TAS: Mario runs, jumps, stomps Goombas, collects coins, and moves through the course automatically. The class supplies the inputs at 20 Python gates on the way to Bowser's castle. The game uses original canvas-drawn pixel art and original sound effects. It does not contain copied Nintendo sprites, music, or level files.

## Run the game

Double-click [`start.bat`](start.bat). It opens the game in the default browser with no installation.

You can also open this file directly:

[`game/index.html`](game/index.html)

Mario's movement is automatic. Click an answer or use number keys `1`–`3` at each gate. Every question has a 20-second countdown. A wrong answer or timeout causes a visible TAS misinput death, then Mario retries from the previous checkpoint. Press `P` to pause between gates. No packages, server, or development-environment setup are required.

## Icebreaker learning objectives

By the end of the game, students can:

- Explain how variables and lists store game state across four questions.
- Predict which branch an `if` statement selects.
- Trace an accumulator through a `for` loop.
- Explain why a `while` loop stops.
- Identify function arguments, parameters, and return values.
- Explain how a class creates objects with independent attributes and shared methods.

## Suggested facilitation: 9:15–9:35

1. **9:15–9:18:** Launch the game and explain that Mario's movement is a tool-assisted speedrun.
2. **9:18–9:30:** Play together as one class. Assign one student to submit each timed input, have everyone vote within 20 seconds, and rotate the controller after each Python world.
3. **9:30–9:33:** Open `game/game.js` and locate one example of a variable, list, condition, loop, and function.
4. **9:33–9:35:** Ask students which concept needs the most practice today.

Wrong answers and timeouts trigger a Mario death animation and count as a TAS misinput. The same concept returns after the checkpoint retry.

## Instructor concept map

| World | Concept | Four-question focus |
| --- | --- | --- |
| 1-1 | Variables and lists | Assignment, `append()`, indexing, and value types |
| 2-1 | Conditions and logic | Comparisons, `if`/`else`, `and`, `or`, and `not` |
| 3-1 | `for` loops | Iteration counts, visible lists, list building, and accumulators |
| 4-1 | `while` loops | Conditions, state changes, stopping, and iteration tracing |
| 5-1 | Functions | Arguments, parameters, return values, and `None` |

## Technical fallback

The earlier terminal version remains in `examples/haunted_mushroom_kingdom.py` as a fallback if a classroom browser cannot open the canvas game.

## Vocabulary

- **Variable:** A name that refers to a stored value.
- **List:** An ordered collection of values.
- **Boolean condition:** An expression that evaluates to `True` or `False`.
- **Accumulator:** A variable updated repeatedly to build a result.
- **`for` loop:** Repeats once for each item in a collection.
- **`while` loop:** Repeats while a condition remains true.
- **Function:** A named, reusable block of code.
- **Argument:** A value supplied when calling a function.
- **Parameter:** A function variable that receives an argument.
- **Return value:** A result sent back to the caller.
- **Class:** A blueprint that groups related data and behavior.
- **Object:** One instance created from a class.
- **Attribute:** A value stored on an object.
- **Method:** A function defined inside a class.

## Guided exercise

After playing, students work in pairs to locate one variable, list, conditional, `for` loop, `while` loop, and function in the source. For each example, they explain what changes if one value is modified.

## Beginner recovery workshop

The main Week 5 lesson uses four browser notebooks. Each module begins with teacher modeling, a silent prediction, a whole-class trace, and one guided change before students work independently. Module 4 is a short, beginner-friendly classes lesson added because the instructor will be out next week.

The print-ready black-and-white reference booklet is in [`python-guide-pdf/`](python-guide-pdf/). The editable Word source and guide generator remain in [`handouts/`](handouts/).

### Student Google Workspace launch

Students do not need to clone the repository or configure Python locally.

1. Click the Colab link for the current module.
2. Sign into the Google account that should own the classwork.
3. Choose **File → Save a copy in Drive**.
4. Rename the copy with the student's name and module number.
5. Work from the saved Google Drive copy for the rest of class.

**Git reminder:** `git pull` downloads new commits from a remote repository into an existing local repository. It does not move a notebook into Google Drive. For this class, the GitHub-to-Colab link replaces the local pull/setup step: GitHub supplies the master notebook, Colab runs it, and **Save a copy in Drive** connects the editable copy to the student's Google account.

Use these current Google Workspace launch links. Each notebook also contains the complete four-module launch panel.

1. [Open Module 1: Game Loadout in Colab](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-05-halloween-loop-quest/exercises/module-1-game-loadout.ipynb) combines variables, lists, loops, multi-part decisions, and a boss function.
2. [Open Module 2: Arcade Loop Trainer in Colab](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-05-halloween-loop-quest/exercises/module-2-arcade-loops.ipynb) practices counters, filtered accumulators, list building, stopping conditions, and multi-output loop challenges.
3. [Open Module 3: Power-Up Functions in Colab](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-05-halloween-loop-quest/exercises/module-3-power-up-functions.ipynb) combines parameters, guarded returns, Boolean decisions, loops inside functions, and multi-result reports.
4. [Open Module 4: Friendly Classes in Colab](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-05-halloween-loop-quest/exercises/module-4-friendly-classes.ipynb) introduces classes, objects, attributes, methods, `__init__`, `self`, independent state, and a small game-object system.

### Saturday agenda

| Time | Block |
| --- | --- |
| 9:00-9:15 | Student arrival, sign-in, browser setup, and settling in |
| 9:15-9:22 | Fast engineering concept review |
| 9:22-9:40 | Mario review game and class voting |
| 9:40-10:25 | Super Mario Debug Quest in Module 1 |
| 10:25-10:35 | Break |
| 10:35-11:20 | Module 2 Arcade Loop Trainer |
| 11:20-11:30 | Break |
| 11:30-12:10 | Module 3 Power-Up Functions |
| 12:10-12:40 | Module 4 Friendly Classes: theory and guided objects |
| 12:40-12:52 | Classes mini-project and peer testing |
| 12:52-1:00 | Exit ticket, sharing, and notebook download |

The editable teaching deck is in `slides/week-05-review-game-labs-v8.pptx`.

## Challenge artifact

Students choose one small extension and demonstrate it to a partner:

- Add a new inventory item and revise the answer choices.
- Add a fourth haunted door.
- Change the coin values and update the trace.
- Write a second function that calculates a bonus.
- Add one attribute and one method to a class from Module 4.

## Peer review

Partners run the modified level, predict the result, and verify that the explanation still matches the code. The reviewer identifies one successful concept and one possible improvement.

## Exit questions

1. When is a `for` loop a better choice than a `while` loop?
2. What must change inside most `while` loops?
3. What is the difference between `print()` and `return`?
4. Which game variable or list represented changing state?
5. When would a class be more useful than a few separate variables?

## Optional extensions

- Add a sixth level that mixes two concepts.
- Store high scores in a text file.
- Randomize the haunted door using the `random` module.
- Add an input-validation function used by every level.
