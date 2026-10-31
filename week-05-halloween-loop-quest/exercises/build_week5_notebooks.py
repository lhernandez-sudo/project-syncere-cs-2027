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

write("module-1-game-loadout.ipynb","Module 1: Super Mario Team Quest",[
    code('''from IPython.display import display, HTML

def mario_scene(title, message, color="#e52521", character="🍄", coins=0):
    coin_row = "🟡 " * coins
    display(HTML(f"""
    <div style="position:relative;overflow:hidden;height:280px;border:8px solid #222;
                border-radius:20px;background:linear-gradient(#55b9ff 0 68%,#73c94b 68% 82%,#b86b32 82%);
                font-family:Arial;text-align:center;color:white;box-shadow:0 10px 0 #222">
      <style>
        @keyframes run {{0%{{left:-10%}} 45%{{left:45%;transform:translateY(0)}} 55%{{left:55%;transform:translateY(-75px)}} 100%{{left:105%;transform:translateY(0)}}}}
        @keyframes pop {{0%,100%{{transform:scale(1)}} 50%{{transform:scale(1.25) rotate(-3deg)}}}}
        @keyframes drift {{from{{transform:translateX(-120px)}} to{{transform:translateX(900px)}}}}
        .runner {{position:absolute;bottom:42px;font-size:64px;animation:run 4s ease-in-out infinite}}
        .cloud {{position:absolute;top:30px;font-size:45px;animation:drift 8s linear infinite}}
      </style>
      <div class="cloud">☁️</div><div class="runner">{character}</div>
      <h1 style="font-size:38px;text-shadow:4px 4px #222;margin:24px 10px 8px">{title}</h1>
      <div style="display:inline-block;background:{color};padding:12px 22px;border:5px solid white;
                  border-radius:14px;font-size:24px;font-weight:bold;animation:pop 1.2s infinite">{message}</div>
      <div style="font-size:25px;margin-top:20px">{coin_row}</div>
    </div>"""))

def checkpoint(name, passed):
    icon = "✅" if passed else "🔁"
    print(f"{icon} {name}: {'CLEARED' if passed else 'TRY AGAIN'}")

mario_scene("MUSHROOM KINGDOM TEAM QUEST", "Choose your crew!", character="🏃", coins=3)'''),
    md('''## Party setup — Teams of 3 or 4

Move next to your teammates. Choose one role now. Rotate after every level.

- **Driver:** edits and runs the code.
- **Navigator:** reads each instruction aloud.
- **Predictor:** announces the result before Run.
- **Reporter:** explains what the team changed.

Every teammate must agree before the Driver presses **Run**.'''),
    md('''## Level 1 — Create your Mario team

Variables are labeled boxes. Your team fills the boxes together.

1. Pick a team name.
2. Choose one character emoji: `🍄`, `⭐`, `🐢`, `👻`, or `🔥`.
3. Choose a team color from the examples.
4. Predict what the cell will display, then run it.'''),
    code('''team_name = "Fire Flower Crew"       # change the text
team_character = "🔥"                  # change the emoji
team_color = "#e52521"                 # try #e52521, #149ece, #43b047, or #fbd000
starting_coins = 3                      # choose 1 through 5

mario_scene(team_name, "TEAM READY!", team_color, team_character, starting_coins)'''),
    md('''### Team checkpoint

The Reporter points to the code and answers:

- Which variable stores text?
- Which variable stores a whole number?
- If `starting_coins` changes, which part of the scene changes?'''),
    code('''checkpoint("Team name is text", type(team_name) == str)
checkpoint("Coins are a whole number", type(starting_coins) == int)
checkpoint("Team selected 1 to 5 coins", starting_coins >= 1 and starting_coins <= 5)'''),
    md('''## Level 2 — Mystery Block Relay

Lists are backpacks that keep several values in order.

1. The Navigator reads the three power-ups.
2. The Predictor chooses which item sits at index `0`.
3. The Driver runs the cell.
4. Everyone performs the action shown on screen.'''),
    code('''power_ups = ["Super Star", "Fire Flower", "Super Mushroom"]
power_icons = ["⭐", "🔥", "🍄"]

print("Power-up at index 0:", power_ups[0])
print("Its matching icon:", power_icons[0])
print("Items in the block:", len(power_ups))'''),
    md('''### Add your own power-up

As a team, invent one classroom-safe power-up and its celebration move. Add it to both lists.'''),
    code('''power_ups.append("Team High Five")
power_icons.append("🙌")

chosen_power = power_ups[-1]
chosen_icon = power_icons[-1]
mario_scene("MYSTERY BLOCK OPEN!", chosen_power, team_color, chosen_icon, len(power_ups))

checkpoint("Both lists match", len(power_ups) == len(power_icons))'''),
    md('''## Level 3 — Coin Rush at 10:00

This is the class photo challenge. Each team sends one Runner to another team.

1. The visiting Runner gives that team a number from 1 to 5.
2. The Driver stores it in `visitor_bonus`.
3. The Predictor calculates the final coins without running.
4. Both teams compare predictions.
5. Run the cell together for the animated reveal.'''),
    code('''coins = starting_coins
visitor_bonus = 4       # visiting student chooses 1 through 5
question_bonus = 3      # team earns this after explaining one variable

print("Start:", coins)
coins = coins + visitor_bonus
print("After visitor bonus:", coins)
coins = coins + question_bonus
print("After question bonus:", coins)

if coins >= 10:
    finish = "SECRET PIPE UNLOCKED!"
    finish_icon = "🌟"
    finish_color = "#43b047"
else:
    finish = "ONE MORE COIN RUSH!"
    finish_icon = "🍄"
    finish_color = "#e52521"

mario_scene(team_name, finish, finish_color, finish_icon, coins)
checkpoint("Coin math", coins == starting_coins + visitor_bonus + question_bonus)'''),
    md('''## Level 4 — Warp Pipe Decision

An `if` condition chooses one path. Teams must negotiate their strategy.

- Blue pipe needs at least 8 coins.
- Green pipe needs a key.
- Gold pipe needs both at least 10 coins **and** a key.

Choose one pipe as a team, then change the variables and run the result.'''),
    code('''chosen_pipe = "gold"     # choose "blue", "green", or "gold"
has_key = True

if chosen_pipe == "gold" and coins >= 10 and has_key:
    pipe_result = "BOWSER CASTLE SHORTCUT!"
    pipe_icon = "🏰"
elif chosen_pipe == "green" and has_key:
    pipe_result = "UNDERGROUND BONUS ROOM!"
    pipe_icon = "🟢"
elif chosen_pipe == "blue" and coins >= 8:
    pipe_result = "SKY WORLD!"
    pipe_icon = "🔵"
else:
    pipe_result = "PIPE LOCKED — CHANGE YOUR PLAN"
    pipe_icon = "🔒"

mario_scene("WARP PIPE RESULT", pipe_result, team_color, pipe_icon, coins)'''),
    md('''## Final boss — Class Castle Battle

Pair with another team. One team becomes **Mario**, and the other becomes **Bowser**.

1. Mario team chooses an attack value from 1 to 5.
2. Bowser team chooses a defense value from 1 to 5.
3. Both Predictors decide whether the attack lands.
4. Run the cell.
5. Switch roles and play again.'''),
    code('''mario_attack = 5       # Mario team chooses 1 through 5
bowser_defense = 3     # Bowser team chooses 1 through 5
team_has_star = True

if mario_attack > bowser_defense and team_has_star:
    battle_result = "BOWSER DEFEATED! CLASS VICTORY!"
    battle_icon = "🏆"
    battle_color = "#fbd000"
else:
    battle_result = "BOWSER BLOCKED IT — PLAN A REMATCH!"
    battle_icon = "🐲"
    battle_color = "#e52521"

mario_scene("FINAL CASTLE BATTLE", battle_result, battle_color, battle_icon, coins)
checkpoint("Attack is a number", type(mario_attack) == int)
checkpoint("Decision produced a result", battle_result != "")'''),
    md('''## Team debrief

Each Reporter shares one sentence:

- “A **variable** changed our game by…”
- “A **list** helped our team store…”
- “The **if condition** chose a result when…”

Save a screenshot of your final castle battle before moving to Module 2.''')
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
