import json
from pathlib import Path

OUT = Path(__file__).parent

def md(text):
    return {"cell_type":"markdown","metadata":{},"source":[line+"\n" for line in text.strip().splitlines()]}

def code(text):
    return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[line+"\n" for line in text.strip().splitlines()]}

def write(name, title, cells):
    intro = md(f'''<div style="background:#071a33;color:white;padding:22px;border-radius:16px">
<h1>{title}</h1><p>Week 5 beginner practice • Read → Predict → Run → Change → Explain</p></div>

**How to work:** Do not rush past a cell you cannot explain. Ask a partner what changes before you press Run.''')
    notebook={"cells":[intro]+cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.12"}},"nbformat":4,"nbformat_minor":5}
    (OUT/name).write_text(json.dumps(notebook,indent=1),encoding="utf-8")

common_setup = code('''def banner(text):
    print("\\n" + "=" * 52)
    print("🎮", text)
    print("=" * 52)

def checkpoint(name, passed):
    icon = "✅" if passed else "🔁"
    print(f"{icon} {name}: {'CLEARED' if passed else 'TRY AGAIN'}")

banner("TRAINING MODE READY")''')

write("module-1-game-loadout.ipynb","Module 1: Build a Game Loadout",[
    common_setup,
    md('''## Level 1 — Variables are labeled boxes

A variable stores one value under a name. Read `coins = 5` as: **put the value 5 in the box named coins**.

### Teacher practice
Before running, point to each variable and say its value and type.'''),
    code('''player_name = "Maya"     # str: text
coins = 5                # int: whole number
has_key = False          # bool: True or False

print(player_name)
print(coins)
print(has_key)'''),
    md('''### Whole-class prediction

What prints after the final line? Trace the box named `coins` after each assignment.'''),
    code('''coins = 5
print("Start:", coins)
coins = coins + 3
print("After treasure:", coins)
coins = coins - 1
print("After the shop:", coins)'''),
    md('''### Guided change

Change the treasure from 3 coins to 10 coins. Predict all three printed values first.'''),
    code('''coins = 5
treasure = 3  # TODO: change this to 10
coins = coins + treasure
coins = coins - 1
print("Final coins:", coins)

checkpoint("Variable update", coins == 7)  # change 7 after you change treasure'''),
    md('''## Level 2 — Lists are backpacks

A list stores several values in order. The first position is index `0`.'''),
    code('''backpack = ["map", "key", "potion"]
print("Whole backpack:", backpack)
print("First item:", backpack[0])
print("Last item:", backpack[-1])
print("Number of items:", len(backpack))'''),
    md('''### Guided practice

1. Predict the list after each line.  
2. Run it.  
3. Change `shield` to an item you would want in a game.'''),
    code('''backpack = ["map", "key"]
backpack.append("shield")
print(backpack)

checkpoint("List grows", len(backpack) == 3)
checkpoint("Key is packed", "key" in backpack)'''),
    md('''## Level 3 — Conditions choose a path

Python runs the indented block only when its condition is `True`. Trace the condition before choosing an answer.'''),
    code('''coins = 8

if coins >= 10:
    message = "You unlocked the gold skin!"
else:
    message = "Collect more coins."

print(message)'''),
    md('''### Pair practice: predict before Run

Test `coins` with 9, 10, and 11. Write which branch runs each time. Why is 10 the boundary?'''),
    code('''coins = 10  # test 9, 10, and 11
has_key = True

if coins >= 10 and has_key:
    result = "BOSS DOOR OPEN"
else:
    result = "DOOR LOCKED"

print(result)
checkpoint("Decision", result == "BOSS DOOR OPEN")'''),
    md('''## Boss challenge — Loadout checker

Complete the condition so a player is ready only when they have a key and at least 2 items.'''),
    code('''player = "Jordan"
inventory = ["key", "potion"]
has_key = "key" in inventory

# TODO: replace True with a condition using has_key and len(inventory)
if True:
    status = "READY"
else:
    status = "KEEP SEARCHING"

print(player, status)
checkpoint("Loadout boss", status == "READY")'''),
    md('''## Exit check

Explain aloud: What is stored in a variable? Why is the first list index 0? How does Python choose an `if` branch?''')
])

write("module-2-arcade-loops.ipynb","Module 2: Arcade Loop Trainer",[
    common_setup,
    md('''## Loop idea — repeat one instruction for every item

Say the loop in plain English first: **For each player in the list, print the player's name.**'''),
    code('''players = ["Ava", "Noah", "Zion"]

for player in players:
    print("Now playing:", player)'''),
    md('''### Human loop practice

Do this without the computer. One student points to each item. Another student says the loop variable. A third counts the iteration.

| Iteration | `player` | Printed line |
|---|---|---|
| 1 | Ava | Now playing: Ava |
| 2 | Noah | Now playing: Noah |
| 3 | Zion | Now playing: Zion |'''),
    md('''## Level 1 — Count iterations

The loop runs once for each list item. Predict `count` after every iteration.'''),
    code('''enemies = ["slime", "ghost", "robot", "dragon"]
count = 0

for enemy in enemies:
    count = count + 1
    print("Iteration", count, "Enemy:", enemy)

print("Total enemies:", count)
checkpoint("Count loop", count == 4)'''),
    md('''### Guided change

Add two enemies. Before running, predict the final count and number of printed battle lines.'''),
    code('''enemies = ["slime", "ghost", "robot"]  # TODO: add two
count = 0
for enemy in enemies:
    count += 1
    print("⚔️ Battle", count, enemy)

print("Battles completed:", count)'''),
    md('''## Level 2 — Accumulators build a total

An accumulator starts with a value and updates during every iteration. Trace `total` one line at a time.'''),
    code('''coin_values = [2, 5, 3]
total = 0

for coin in coin_values:
    print("Before:", total, "+", coin)
    total = total + coin
    print("After:", total)

checkpoint("Coin total", total == 10)'''),
    md('''### Trace before Run

Fill this in on paper: `0 → ___ → ___ → ___` for `[4, 1, 6]`.'''),
    code('''scores = [4, 1, 6]
total = 0
for score in scores:
    total += score

print("Team score:", total)
checkpoint("Score accumulator", total == 11)'''),
    md('''## Level 3 — Build a new list

Start with an empty list. The loop creates and appends one new value per iteration.'''),
    code('''base_damage = [2, 4, 6]
powered_damage = []

for damage in base_damage:
    powered_damage.append(damage * 2)

print(powered_damage)
checkpoint("Power list", powered_damage == [4, 8, 12])'''),
    md('''## Level 4 — While loops need an exit

Ask two questions: **What keeps the loop running? What changes so it stops?**'''),
    code('''energy = 3

while energy > 0:
    print("🏃 Energy:", energy)
    energy = energy - 1

print("REST")
checkpoint("While loop stops", energy == 0)'''),
    md('''### Repair challenge

This starter is safe, but incomplete. Add one line inside the loop that changes `turns_left` so the game ends.'''),
    code('''turns_left = 4

while turns_left > 0:
    print("Turn", turns_left)
    # TODO: subtract 1 from turns_left
    break  # remove this after adding the update

print("Game over")'''),
    md('''## Boss challenge — Arcade scoreboard

Use one loop to count games, total the scores, and print whether each score earned a bonus.'''),
    code('''scores = [8, 12, 5, 15]
games_played = 0
total_score = 0

for score in scores:
    games_played += 1
    total_score += score
    if score >= 10:
        print("🔥 BONUS ROUND:", score)
    else:
        print("Score:", score)

print("Games:", games_played)
print("Total:", total_score)
checkpoint("Loop boss count", games_played == 4)
checkpoint("Loop boss total", total_score == 40)'''),
    md('''## Loop mastery check

Point to the loop variable, collection, repeated block, accumulator, and stopping condition. Explain each without reading the definition.''')
])

write("module-3-power-up-functions.ipynb","Module 3: Power-Up Function Factory",[
    common_setup,
    md('''## Function idea — name a reusable job

Python remembers the recipe after `def`. The code runs only when you call the function.'''),
    code('''def cheer():
    print("🎉 LEVEL UP!")

cheer()
cheer()'''),
    md('''## Level 1 — Parameters receive arguments

Trace the call `greet_player("Ari")`: the argument `"Ari"` moves into the parameter `name`.'''),
    code('''def greet_player(name):
    print("Welcome,", name)

greet_player("Ari")
greet_player("Sam")'''),
    md('''### Guided change

Add a second parameter named `game`. Update both calls.'''),
    code('''def player_card(name, score):
    print("Player:", name)
    print("Score:", score)

player_card("Maya", 12)
player_card("Devin", 18)'''),
    md('''## Level 2 — Return sends a value back

`print()` shows a value. `return` gives a value back to the calling code so it can be saved or reused.'''),
    code('''def add_bonus(score, bonus):
    new_score = score + bonus
    return new_score

final_score = add_bonus(10, 5)
print("Final:", final_score)
checkpoint("Return value", final_score == 15)'''),
    md('''### Predict three parts

1. Arguments: `7` and `3`  
2. Parameters: `damage` and `armor`  
3. Returned value: ?'''),
    code('''def hit_points(damage, armor):
    result = damage - armor
    return result

points_lost = hit_points(7, 3)
print(points_lost)
checkpoint("Function trace", points_lost == 4)'''),
    md('''## Level 3 — Functions can contain decisions'''),
    code('''def rank_player(score):
    if score >= 20:
        return "GOLD"
    elif score >= 10:
        return "SILVER"
    else:
        return "BRONZE"

print(rank_player(8))
print(rank_player(14))
print(rank_player(25))'''),
    md('''## Level 4 — Functions can contain loops

Trace `total` after every score before running.'''),
    code('''def total_scores(scores):
    total = 0
    for score in scores:
        total += score
    return total

team_total = total_scores([4, 6, 5])
print(team_total)
checkpoint("Function loop", team_total == 15)'''),
    md('''## Boss challenge — Battle report

Complete `average_score`. Then call both functions to create a report.'''),
    code('''def average_score(scores):
    total = 0
    for score in scores:
        total += score
    # TODO: return total divided by the number of scores
    return 0

def battle_message(average):
    if average >= 10:
        return "BOSS DEFEATED"
    return "TRAIN AND RETRY"

battle_scores = [8, 12, 10]
average = average_score(battle_scores)
message = battle_message(average)
print("Average:", average)
print(message)

# This passes after average_score is complete.
checkpoint("Function boss", average == 10 and message == "BOSS DEFEATED")'''),
    md('''## Exit check

Draw arrows from argument → parameter → local variable → return value. Explain why a function with no `return` gives `None`.''')
])

print("Created Week 5 notebooks")
