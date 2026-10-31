import json
from pathlib import Path

OUT = Path(__file__).parent

def md(text):
    return {"cell_type":"markdown","metadata":{},"source":[line+"\n" for line in text.strip().splitlines()]}

def code(text):
    return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[line+"\n" for line in text.strip().splitlines()]}

def write(name, title, cells):
    colab_url = f"https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-05-halloween-loop-quest/exercises/{name}"
    intro = md(f'''<div style="background:#071a33;color:white;padding:22px;border-radius:16px">
<h1>{title}</h1><p>Week 5 beginner practice • Read → Predict → Run → Change → Explain</p></div>

## Open and save your Google Workspace copy

[**Open this notebook in Google Colab**]({colab_url})

1. Sign into the Google account you will use for class.
2. In Colab, choose **File → Save a copy in Drive**.
3. Rename the copy with your name and the module number.
4. Confirm that **Copy of** no longer appears in the title.
5. Complete the lesson in your saved Google Drive copy.

> **Git reminder:** `git pull` downloads the newest repository changes to a local computer. We are not using `git pull` for today's labs. The GitHub-to-Colab link opens the newest notebook in your browser, and **Save a copy in Drive** puts your editable copy in your Google account.

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

write("module-1-game-loadout.ipynb","Module 1: Super Mario Debug Quest",[
    code('''from IPython.display import display, HTML

def mario_level(title, goal, success, reason, character="🍄", enemy="🐢", coins=0):
    state = "win" if success else "fail"
    headline = "LEVEL CLEAR!" if success else "MARIO MISSED THE CODE!"
    detail = goal if success else reason
    color = "#25a244" if success else "#d00000"
    coin_row = "🟡 " * min(coins, 12)
    display(HTML(f"""
    <div class="mario-stage {state}">
      <style>
        .mario-stage {{position:relative;overflow:hidden;height:360px;border:8px solid #111;border-radius:18px;
          background:linear-gradient(#45b6ff 0 67%,#71c837 67% 80%,#b7652a 80%);font-family:Arial;color:white;
          text-align:center;box-shadow:0 12px 0 #222}}
        .mario-stage:after {{content:'';position:absolute;left:0;right:0;bottom:58px;height:12px;
          background:repeating-linear-gradient(90deg,#d98b3a 0 38px,#6b3217 38px 42px)}}
        @keyframes cloudMove {{from{{left:-120px}}to{{left:105%}}}}
        @keyframes winRun {{0%{{left:-10%;bottom:70px}}35%{{left:32%;bottom:70px}}55%{{left:52%;bottom:180px;transform:rotate(-12deg)}}75%{{left:70%;bottom:70px}}100%{{left:92%;bottom:70px}}}}
        @keyframes failRun {{0%{{left:-10%;bottom:70px;transform:rotate(0)}}55%{{left:49%;bottom:70px;transform:rotate(0)}}65%{{left:52%;bottom:76px;transform:rotate(-25deg)}}75%{{left:52%;bottom:145px;transform:rotate(180deg)}}100%{{left:52%;bottom:-100px;transform:rotate(540deg)}}}}
        @keyframes enemyMove {{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(-35px)}}}}
        @keyframes flagRise {{0%{{height:0;opacity:0}}70%{{height:0;opacity:0}}100%{{height:150px;opacity:1}}}}
        @keyframes flash {{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
        @keyframes shake {{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-8px)}}75%{{transform:translateX(8px)}}}}
        .sky-title {{position:relative;z-index:5;margin:18px 12px 5px;font-size:32px;text-shadow:4px 4px #222}}
        .mission {{position:relative;z-index:5;font-size:18px;font-weight:bold}}
        .runner {{position:absolute;z-index:4;font-size:64px;animation:{'winRun' if success else 'failRun'} 4.4s ease-in-out infinite}}
        .enemy {{position:absolute;z-index:3;left:55%;bottom:70px;font-size:58px;animation:enemyMove 1s infinite}}
        .cloud {{position:absolute;top:86px;font-size:44px;animation:cloudMove 9s linear infinite}}
        .flag {{position:absolute;right:8%;bottom:70px;width:10px;background:white;animation:flagRise 4.4s infinite}}
        .result {{position:absolute;z-index:8;left:10%;right:10%;top:145px;background:{color};border:6px solid white;
          border-radius:12px;padding:10px;font-size:25px;font-weight:bold;
          animation:{'flash' if success else 'shake'} .8s infinite}}
        .coins {{position:absolute;z-index:6;left:0;right:0;bottom:15px;font-size:21px}}
      </style>
      <div class="cloud">☁️</div><div class="sky-title">{title}</div><div class="mission">MISSION: {goal}</div>
      <div class="runner">{character}</div><div class="enemy">{enemy}</div><div class="flag"></div>
      <div class="result">{headline}<br><span style="font-size:17px">{detail}</span></div><div class="coins">{coin_row}</div>
    </div>"""))

def checkpoint(name, passed):
    icon = "✅" if passed else "🔁"
    print(f"{icon} {name}: {'CLEARED' if passed else 'FIX THE CODE AND RUN AGAIN'}")

mario_level("WORLD 1-1", "Repair the code to reach the flag", False,
            "The starter code is supposed to fail. Your team will fix it.", character="🏃")'''),
    md('''## Team roles

Work in teams of 3 or 4. Rotate roles after every level.

- **Driver:** changes the code and presses Run.
- **Navigator:** reads the mission and tips aloud.
- **Predictor:** says whether Mario will live or die before Run.
- **Debugger:** points to the exact variable, list item, or condition that needs repair.

The first run should fail. A failure animation means the code gave you useful information.'''),
    md('''## Level 1 — Jump Power Variable

**Concept reminder:** A variable stores one value under a name. Changing the value changes what the program can do.

**Mission:** Mario needs jump power of at least `3` to clear the Goomba.

Run the starter once. Watch Mario fail. Then repair only the value stored in `jump_power`.

**Tips**

- Look for the line with `jump_power =`.
- Keep the variable name the same.
- Replace only the number.'''),
    code('''team_name = "Fire Flower Crew"
jump_power = 1          # TODO: Mario needs at least 3

can_jump = jump_power >= 3
mario_level("LEVEL 1: GOOMBA JUMP", "Set jump_power to 3 or more", can_jump,
            "Jump power was too low. Change the variable and retry.",
            character="🏃", enemy="🍄", coins=jump_power)
checkpoint("Jump power", can_jump)'''),
    md('''### Explain the repair

The Predictor completes this sentence before the team moves on:

> Mario failed because `jump_power` stored ____. We changed it to ____ so the condition became `True`.'''),
    md('''## Level 2 — Power-Up List

**Concept reminder:** A list stores several values in order. `.append()` adds one value to the end.

**Mission:** Mario can survive the Koopa only when `"Super Mushroom"` is inside the inventory list.

Run the starter, inspect the printed list, then add the missing item.

**Tips**

- Do not replace the entire list.
- Remove `#` from the TODO line so Python runs it.
- The spelling and capitalization must match exactly.'''),
    code('''inventory = ["coin", "map"]

# TODO: remove the # from the next line
# inventory.append("Super Mushroom")

has_mushroom = "Super Mushroom" in inventory
print("Current inventory:", inventory)
mario_level("LEVEL 2: KOOPA ROAD", "Put Super Mushroom in inventory", has_mushroom,
            "Mario was small. Use append() to add the missing power-up.",
            character="🏃", enemy="🐢", coins=len(inventory))
checkpoint("Power-up list", has_mushroom)'''),
    md('''### Partner check

The Debugger points to:

1. The list variable.
2. The value added by `.append()`.
3. The condition that checks whether the value is in the list.'''),
    md('''## Level 3 — Coin Rush at 10:00

**Concept reminder:** A variable can be updated using its old value: `coins = coins + bonus`.

**Mission:** Reach at least `10` coins to unlock the secret pipe.

Send one teammate to another team. The visiting student chooses `visitor_bonus` from 1 to 5. Both teams calculate the total before Run.

**Tips**

- Trace the value after every update.
- You may change `visitor_bonus` and `question_bonus`.
- The final value must make `coins >= 10` true.'''),
    code('''coins = 2
visitor_bonus = 2       # TODO: visiting student may change this
question_bonus = 1      # TODO: increase after explaining the coin updates

print("Start:", coins)
coins = coins + visitor_bonus
print("After visitor bonus:", coins)
coins = coins + question_bonus
print("After question bonus:", coins)

pipe_unlocked = coins >= 10
mario_level("LEVEL 3: COIN RUSH", "Reach 10 coins", pipe_unlocked,
            "The pipe stayed locked. Trace the updates and raise the bonuses.",
            character="🏃", enemy="🕳️", coins=coins)
checkpoint("Coin total", pipe_unlocked)'''),
    md('''## Level 4 — Repair the If Condition

**Concept reminder:** An `if` statement runs its indented block only when the condition is `True`. `and` requires both sides to be true.

**Mission:** Open the castle door when Mario has at least 10 coins **and** has the key.

The starter uses `False`, so Mario always dies. Replace `False` with the correct condition.

**Tips**

- First comparison: `coins >= 10`
- Second condition: `has_key`
- Join them with `and`.
- Your finished line begins with `if coins`.'''),
    code('''has_key = True

# TODO: replace False with a condition using coins, has_key, and and
if False:
    castle_open = True
else:
    castle_open = False

mario_level("LEVEL 4: CASTLE DOOR", "Use coins and the key", castle_open,
            "The condition sent Mario into the lava. Repair the if line.",
            character="🏃", enemy="🔥", coins=coins)
checkpoint("Castle condition", castle_open)'''),
    md('''### Condition trace

The Reporter explains both sides separately:

- `coins >= 10` is ____.
- `has_key` is ____.
- `True and True` becomes ____.'''),
    md('''## Final Boss — Bowser Condition

Pair with another team. One team controls Mario's attack. The other controls Bowser's defense.

**Mission:** Mario wins only when his attack is greater than Bowser's defense **and** he has a star.

The condition is broken on purpose. Repair it, predict the outcome, and run the battle.

**Tips**

- Compare `mario_attack` and `bowser_defense` with `>`.
- Check `team_has_star` in the same condition.
- Use `and` because both requirements matter.
- If Mario still dies, print the three variable values and compare them.'''),
    code('''mario_attack = 5
bowser_defense = 3
team_has_star = True

# TODO: replace False with the complete boss condition
if False:
    bowser_defeated = True
else:
    bowser_defeated = False

print("Mario attack:", mario_attack)
print("Bowser defense:", bowser_defense)
print("Team has star:", team_has_star)
mario_level("FINAL BOSS: BOWSER", "Win with attack AND a star", bowser_defeated,
            "Bowser's fireball hit Mario. Repair the two-part condition.",
            character="🏃", enemy="🐲", coins=coins)
checkpoint("Bowser battle", bowser_defeated)'''),
    md('''## Final team debrief

Each Reporter shares one repair:

- “We changed the **variable** because…”
- “We added to the **list** because…”
- “Our **if condition** needed `and` because…”

Save a screenshot of the successful Bowser battle in your Google Drive copy. If the final animation still shows Mario dying, do not move on yet. Ask another team to trace your condition.''')
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
