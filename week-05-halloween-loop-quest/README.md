# Week 5 Icebreaker: Super Mario Haunted Python Kingdom

This unofficial, fan-made Super Mario Halloween terminal game reviews the Week 3 and Week 4 Python foundations before students begin independent work. It features Mario, Toad, Boo, Bowser, Peach, warp pipes, coins, and power-ups. It uses original text art, six terminal colors, and only the Python standard library. It does not contain copied Nintendo sprites, music, or level files.

## Run the game

From the repository root:

```powershell
py -3 week-05-halloween-loop-quest/examples/haunted_mushroom_kingdom.py
```

On Windows, you can also double-click [`start.bat`](start.bat).

No packages or development-environment setup are required.

## Icebreaker learning objectives

By the end of the game, students can:

- Explain how variables and lists store game state.
- Predict which branch an `if` statement selects.
- Trace an accumulator through a `for` loop.
- Explain why a `while` loop stops.
- Identify function arguments, parameters, and return values.

## Suggested facilitation: 9:00–9:25

1. **9:00–9:03:** Launch the game and let students choose the player name.
2. **9:03–9:18:** Let the class vote on each answer. Ask for a prediction before entering it.
3. **9:18–9:22:** Open the source file and find one example of each concept in the actual game.
4. **9:22–9:25:** Ask students which concept needs the most practice today.

Wrong answers do not end the game. They award fewer coins and display an explanation, keeping the activity useful for a mixed-confidence group.

## Instructor concept map

| Level | Concept | Key question |
| --- | --- | --- |
| Toad's Inventory Pipe | Variables and lists | How do `append()` and `len()` change or inspect a list? |
| Boo's Haunted House | Conditions and logic | How do `and` and `not` combine Boolean values? |
| Super Mario Coin Road | `for` loops | How does an accumulator change each iteration? |
| Warp Pipe Maze | `while` loops | Which state change makes the loop condition false? |
| Bowser's Function Castle | Functions | How do arguments become parameters and produce a return value? |

## Quick technical check

```powershell
py -3 week-05-halloween-loop-quest/examples/haunted_mushroom_kingdom.py --self-test
```

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

## Guided exercise

After playing, students work in pairs to locate one variable, list, conditional, `for` loop, `while` loop, and function in the source. For each example, they explain what changes if one value is modified.

## Challenge artifact

Students choose one small extension and demonstrate it to a partner:

- Add a new inventory item and revise the answer choices.
- Add a fourth haunted door.
- Change the coin values and update the trace.
- Write a second function that calculates a bonus.

## Peer review

Partners run the modified level, predict the result, and verify that the explanation still matches the code. The reviewer identifies one successful concept and one possible improvement.

## Exit questions

1. When is a `for` loop a better choice than a `while` loop?
2. What must change inside most `while` loops?
3. What is the difference between `print()` and `return`?
4. Which game variable or list represented changing state?

## Optional extensions

- Add a sixth level that mixes two concepts.
- Store high scores in a text file.
- Randomize the haunted door using the `random` module.
- Add an input-validation function used by every level.
