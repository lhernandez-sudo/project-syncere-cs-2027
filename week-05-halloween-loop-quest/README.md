# Week 5 Icebreaker: Super Mario Haunted Python Kingdom

This unofficial, fan-made Super Mario Halloween side-scroller reviews the Week 3 and Week 4 Python foundations. It plays like a classroom TAS: Mario runs, jumps, stomps Goombas, collects coins, and moves through the course automatically. The class supplies the inputs at 20 Python gates on the way to Bowser's castle. The game uses original canvas-drawn pixel art and original sound effects. It does not contain copied Nintendo sprites, music, or level files.

## Run the game

Double-click [`start.bat`](start.bat). It opens the game in the default browser with no installation.

You can also open this file directly:

[`game/index.html`](game/index.html)

Mario's movement is automatic. Click an answer or use number keys `1`–`3` at each gate. Every question has a 15-second countdown. A wrong answer or timeout causes a visible TAS misinput death, then Mario retries from the previous checkpoint. Press `P` to pause between gates. No packages, server, or development-environment setup are required.

## Icebreaker learning objectives

By the end of the game, students can:

- Explain how variables and lists store game state across four questions.
- Predict which branch an `if` statement selects.
- Trace an accumulator through a `for` loop.
- Explain why a `while` loop stops.
- Identify function arguments, parameters, and return values.

## Suggested facilitation: 9:00–9:25

1. **9:00–9:03:** Launch the game and explain that Mario's movement is a tool-assisted speedrun.
2. **9:03–9:18:** Assign a student to submit each timed input. At every gate, the class has 15 seconds to vote before the input is entered.
3. **9:18–9:22:** Open `game/game.js` and locate one example of a variable, list, condition, loop, and function.
4. **9:22–9:25:** Ask students which concept needs the most practice today.

Wrong answers and timeouts trigger a Mario death animation and count as a TAS misinput. The same concept returns after the checkpoint retry.

## Instructor concept map

| World | Concept | Four-question focus |
| --- | --- | --- |
| 1-1 | Variables and lists | Assignment, `append()`, indexing, and value types |
| 2-1 | Conditions and logic | Comparisons, `if`/`else`, `and`, `or`, and `not` |
| 3-1 | `for` loops | Iteration counts, ranges, list building, and accumulators |
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
