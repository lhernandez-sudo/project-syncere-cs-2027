# Week 5 Icebreaker: Super Mario Haunted Python Kingdom

This unofficial, fan-made Super Mario Halloween side-scroller reviews the Week 3 and Week 4 Python foundations. Students run, jump, stomp Goombas, collect coins, hit question blocks, enter warp pipes, and unlock five Python gates on the way to Bowser's castle. The game uses original canvas-drawn pixel art and original sound effects. It does not contain copied Nintendo sprites, music, or level files.

## Run the game

Double-click [`start.bat`](start.bat). It opens the game in the default browser with no installation.

You can also open this file directly:

[`game/index.html`](game/index.html)

Controls: arrow keys or `A`/`D` to run, Space/Up/`W` to jump, and `P` to pause. Number keys `1`–`3` answer Python gates. No packages, server, or development-environment setup are required.

## Icebreaker learning objectives

By the end of the game, students can:

- Explain how variables and lists store game state.
- Predict which branch an `if` statement selects.
- Trace an accumulator through a `for` loop.
- Explain why a `while` loop stops.
- Identify function arguments, parameters, and return values.

## Suggested facilitation: 9:00–9:25

1. **9:00–9:03:** Launch the game and demonstrate run, jump, and Goomba stomping.
2. **9:03–9:18:** Let students take turns playing. At each locked gate, let the class vote before choosing an answer.
3. **9:18–9:22:** Open `game/game.js` and locate one example of a variable, list, condition, loop, and function.
4. **9:22–9:25:** Ask students which concept needs the most practice today.

Wrong gate answers do not end the game. The gate asks students to trace the code and try again.

## Instructor concept map

| Level | Concept | Key question |
| --- | --- | --- |
| Toad's Inventory Pipe | Variables and lists | How do `append()` and `len()` change or inspect a list? |
| Boo's Haunted House | Conditions and logic | How do `and` and `not` combine Boolean values? |
| Super Mario Coin Road | `for` loops | How does an accumulator change each iteration? |
| Warp Pipe Maze | `while` loops | Which state change makes the loop condition false? |
| Bowser's Function Castle | Functions | How do arguments become parameters and produce a return value? |

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
