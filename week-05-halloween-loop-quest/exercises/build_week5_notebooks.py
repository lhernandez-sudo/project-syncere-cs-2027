import json
from pathlib import Path

OUT = Path(__file__).parent

def md(text):
    return {"cell_type":"markdown","metadata":{},"source":[line+"\n" for line in text.strip().splitlines()]}

def code(text):
    return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[line+"\n" for line in text.strip().splitlines()]}

def write(name, title, cells):
    colab_url = f"https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-05-halloween-loop-quest/exercises/{name}"
    module_links = """[Module 1: Debug Quest](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-05-halloween-loop-quest/exercises/module-1-game-loadout.ipynb) · [Module 2: Loop Trainer](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-05-halloween-loop-quest/exercises/module-2-arcade-loops.ipynb) · [Module 3: Function Factory](https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-05-halloween-loop-quest/exercises/module-3-power-up-functions.ipynb)"""
    intro = md(f'''<div style="background:#071a33;color:white;padding:22px;border-radius:16px">
<h1>{title}</h1><p>Week 5 beginner practice • Read → Predict → Run → Change → Explain</p></div>

## Open and save your Google Workspace copy

[**Open this notebook in Google Colab**]({colab_url})

### Week 5 Google Workspace launch pad

{module_links}

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

def integrity_check(name, rules):
    """Require every named rule to pass and explain exactly what failed."""
    failed = [message for passed, message in rules if not passed]
    checkpoint(name, not failed)
    for message in failed:
        print("   ↳", message)
    return not failed

banner("TRAINING MODE READY")''')

write("module-1-game-loadout.ipynb","Module 1: Super Mario Debug Quest",[
    code('''from IPython.display import display, HTML, Audio
import io
import math
import struct
import wave

def mario_level(title, goal, success, reason, character="🍄", enemy="🐢", coins=0):
    state = "win" if success else "fail"
    headline = "LEVEL CLEAR!" if success else "MARIO MISSED THE CODE!"
    detail = goal if success else reason
    color = "#25a244" if success else "#d00000"
    coin_row = "🟡 " * min(coins, 12)
    display(HTML(f"""
    <div class="mario-stage {state}">
      <style>
        .mario-stage {{position:relative;overflow:hidden;height:390px;border:8px solid #111;border-radius:18px;
          background:linear-gradient(#45b6ff 0 67%,#71c837 67% 80%,#b7652a 80%);font-family:Arial;color:white;
          text-align:center;box-shadow:0 12px 0 #222}}
        .mario-stage:after {{content:'';position:absolute;left:0;right:0;bottom:58px;height:12px;
          background:repeating-linear-gradient(90deg,#d98b3a 0 38px,#6b3217 38px 42px)}}
        @keyframes cloudMove {{from{{left:-120px}}to{{left:105%}}}}
        @keyframes winRun {{0%{{left:-9%;bottom:70px}}38%{{left:34%;bottom:70px}}52%{{left:53%;bottom:190px;transform:rotate(-8deg)}}68%{{left:69%;bottom:70px}}100%{{left:94%;bottom:70px}}}}
        @keyframes failRun {{0%{{left:-9%;bottom:70px;transform:rotate(0)}}48%{{left:43%;bottom:70px;transform:rotate(0)}}58%{{left:50%;bottom:84px;transform:rotate(-18deg)}}70%{{left:52%;bottom:155px;transform:rotate(165deg)}}100%{{left:55%;bottom:-105px;transform:rotate(520deg)}}}}
        @keyframes legs {{0%,100%{{transform:rotate(28deg)}}50%{{transform:rotate(-28deg)}}}}
        @keyframes arms {{0%,100%{{transform:rotate(-32deg)}}50%{{transform:rotate(32deg)}}}}
        @keyframes bob {{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
        @keyframes enemyMove {{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(-35px)}}}}
        @keyframes flagRise {{0%{{height:0;opacity:0}}70%{{height:0;opacity:0}}100%{{height:150px;opacity:1}}}}
        @keyframes flash {{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
        @keyframes shake {{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-8px)}}75%{{transform:translateX(8px)}}}}
        .sky-title {{position:relative;z-index:5;margin:18px 12px 5px;font-size:32px;text-shadow:4px 4px #222}}
        .mission {{position:relative;z-index:5;font-size:18px;font-weight:bold}}
        .runner {{position:absolute;z-index:4;width:62px;height:88px;animation:{'winRun' if success else 'failRun'} 3.2s cubic-bezier(.4,0,.35,1) infinite}}
        .hero-body {{position:absolute;left:15px;top:35px;width:34px;height:37px;background:#1769c2;border:4px solid #111;border-radius:9px;animation:bob .28s infinite}}
        .hero-head {{position:absolute;left:17px;top:8px;width:37px;height:32px;background:#f2aa6b;border:4px solid #111;border-radius:45%}}
        .hero-cap {{position:absolute;left:10px;top:0;width:43px;height:17px;background:#e52b32;border:4px solid #111;border-radius:18px 18px 5px 5px}}
        .hero-cap:after {{content:'M';position:absolute;left:15px;top:-2px;color:white;font:bold 13px Arial}}
        .hero-eye {{position:absolute;left:43px;top:18px;width:5px;height:7px;background:#111}}
        .hero-nose {{position:absolute;left:49px;top:24px;width:13px;height:10px;background:#f2aa6b;border:3px solid #111;border-radius:50%}}
        .hero-mustache {{position:absolute;left:39px;top:33px;width:19px;height:7px;background:#442513;border-radius:50%}}
        .strap {{position:absolute;top:37px;width:5px;height:22px;background:#5eb0ff}} .strap.a {{left:22px}} .strap.b {{left:40px}}
        .button {{position:absolute;top:47px;width:5px;height:5px;background:#ffd43b;border-radius:50%}} .button.a {{left:24px}} .button.b {{left:41px}}
        .arm,.leg {{position:absolute;transform-origin:top center;border:4px solid #111}}
        .arm {{top:43px;width:10px;height:28px;background:#e52b32;animation:arms .28s infinite}} .arm.a {{left:7px}} .arm.b {{left:49px;animation-direction:reverse}}
        .glove {{position:absolute;bottom:-8px;left:-5px;width:14px;height:12px;background:white;border:3px solid #111;border-radius:50%}}
        .leg {{top:67px;width:12px;height:25px;background:#1769c2;animation:legs .28s infinite}} .leg.a {{left:20px}} .leg.b {{left:38px;animation-direction:reverse}}
        .shoe {{position:absolute;bottom:-7px;left:-5px;width:19px;height:10px;background:#71391f;border:3px solid #111;border-radius:50%}}
        .enemy {{position:absolute;z-index:3;left:55%;bottom:70px;font-size:58px;animation:enemyMove 1s infinite}}
        .cloud {{position:absolute;top:86px;font-size:44px;animation:cloudMove 9s linear infinite}}
        .flag {{position:absolute;right:8%;bottom:70px;width:10px;background:white;animation:flagRise 4.4s infinite}}
        .result {{position:absolute;z-index:8;left:16%;right:16%;bottom:12px;background:{color};border:5px solid white;
          border-radius:12px;padding:8px;font-size:23px;font-weight:bold;
          animation:{'flash' if success else 'shake'} .8s infinite}}
        .coins {{position:absolute;z-index:6;right:15px;top:92px;font-size:20px}}
      </style>
      <div class="cloud">☁️</div><div class="sky-title">{title}</div><div class="mission">MISSION: {goal}</div>
      <div class="runner"><div class="hero-cap"></div><div class="hero-head"></div><div class="hero-eye"></div><div class="hero-nose"></div><div class="hero-mustache"></div><div class="hero-body"></div><div class="strap a"></div><div class="strap b"></div><div class="button a"></div><div class="button b"></div><div class="arm a"><div class="glove"></div></div><div class="arm b"><div class="glove"></div></div><div class="leg a"><div class="shoe"></div></div><div class="leg b"><div class="shoe"></div></div></div><div class="enemy">{enemy}</div><div class="flag"></div>
      <div class="result">{headline}<br><span style="font-size:17px">{detail}</span></div><div class="coins">{coin_row}</div>
    </div>"""))

def checkpoint(name, passed):
    icon = "✅" if passed else "🔁"
    print(f"{icon} {name}: {'CLEARED' if passed else 'FIX THE CODE AND RUN AGAIN'}")

def integrity_check(name, rules):
    """Run several anti-shortcut checks and show actionable feedback."""
    failed = [message for passed, message in rules if not passed]
    checkpoint(name, not failed)
    for message in failed:
        print("   ↳", message)
    return not failed

def make_chiptune():
    """Create an original arcade-style soundtrack without external files."""
    sample_rate = 11025
    beat = 0.14
    melody = [
        659, 784, 988, 784, 659, 523, 587, 659,
        698, 880, 1047, 880, 698, 587, 659, 698,
        784, 988, 1175, 988, 784, 659, 698, 784,
        523, 659, 784, 659, 587, 494, 523, 0,
    ]
    bass = [131, 131, 196, 196, 147, 147, 220, 220]
    frames = []
    for repeat in [1, 2, 3, 4]:
        note_number = 0
        for frequency in melody:
            bass_frequency = bass[note_number % len(bass)]
            sample = 0
            while sample < int(sample_rate * beat):
                time = sample / sample_rate
                lead = 0 if frequency == 0 else (1 if math.sin(2 * math.pi * frequency * time) >= 0 else -1)
                low = 1 if math.sin(2 * math.pi * bass_frequency * time) >= 0 else -1
                pulse = 1 if math.sin(2 * math.pi * (frequency * 2 if frequency else 1) * time) >= 0 else -1
                fade = 1 - (sample / (sample_rate * beat)) * 0.35
                value = int(10500 * fade * (0.62 * lead + 0.28 * low + 0.10 * pulse))
                frames.append(struct.pack("<h", value))
                sample = sample + 1
            note_number = note_number + 1
    audio_file = io.BytesIO()
    with wave.open(audio_file, "wb") as sound:
        sound.setnchannels(1)
        sound.setsampwidth(2)
        sound.setframerate(sample_rate)
        sound.writeframes(b"".join(frames))
    return audio_file.getvalue()

display(HTML("""
<div style="background:#111;color:white;border:5px solid #fbd000;border-radius:14px;
padding:14px;text-align:center;font-family:Arial;font-size:20px;font-weight:bold">
🎵 SOUNDTRACK READY — Click Play, then begin World 1-1
</div>
"""))
display(Audio(make_chiptune(), autoplay=False))

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

**Mission:** Mario needs jump power of at least `3` **and** run speed of at least `2` to clear the Goomba.

Run the starter once. Watch Mario fail. Then repair only the value stored in `jump_power`.

**Tips**

- Look for the line with `jump_power =`.
- Keep the variable name the same.
- Repair both values, then explain why `and` needs both comparisons to be `True`.'''),
    code('''team_name = "Fire Flower Crew"
jump_power = 1          # TODO: Mario needs at least 3
run_speed = 1           # TODO: Mario needs at least 2

can_clear_goomba = jump_power >= 3 and run_speed >= 2
movement_valid = integrity_check("Movement integrity", [
    (type(jump_power) is int, "jump_power must be an integer, not text or True/False."),
    (type(run_speed) is int, "run_speed must be an integer, not text or True/False."),
    (3 <= jump_power <= 10, "Use a reasonable jump_power from 3 through 10."),
    (2 <= run_speed <= 10, "Use a reasonable run_speed from 2 through 10."),
])
can_clear_goomba = can_clear_goomba and movement_valid
mario_level("LEVEL 1: GOOMBA JUMP", "Repair power AND speed", can_clear_goomba,
            "One of the two movement variables is still too low.",
            enemy="🍄", coins=jump_power + run_speed)
checkpoint("Movement system", can_clear_goomba)'''),
    md('''### Explain the repair

The Predictor completes this sentence before the team moves on:

> Mario failed because `jump_power` stored ____ and `run_speed` stored ____. We changed them to ____ and ____ so both sides became `True`.'''),
    md('''## Level 2 — Power-Up List

**Concept reminder:** A list stores several values in order. `.append()` adds one value to the end.

**Mission:** Mario needs both `"Super Mushroom"` and `"Fire Flower"` in the inventory list.

Run the starter, inspect the printed list, then add the missing item.

**Tips**

- Do not replace the entire list.
- Remove `#` from the TODO line so Python runs it.
- The spelling and capitalization must match exactly.'''),
    code('''inventory = ["coin", "map"]

# TODO: uncomment this line and add a second append for Fire Flower
# inventory.append("Super Mushroom")

has_mushroom = "Super Mushroom" in inventory
has_fire_flower = "Fire Flower" in inventory
loadout_ready = has_mushroom and has_fire_flower
loadout_valid = integrity_check("Inventory integrity", [
    (type(inventory) is list, "inventory must remain a list."),
    (type(inventory) is list and inventory[:2] == ["coin", "map"], "Keep the original coin and map in order."),
    (type(inventory) is list and inventory.count("Super Mushroom") == 1, "Add exactly one Super Mushroom."),
    (type(inventory) is list and inventory.count("Fire Flower") == 1, "Add exactly one Fire Flower."),
])
loadout_ready = loadout_ready and loadout_valid
print("Current inventory:", inventory)
mario_level("LEVEL 2: KOOPA ROAD", "Build a two-item power loadout", loadout_ready,
            "The loadout needs both named power-ups. Inspect both Boolean checks.",
            enemy="🐢", coins=len(inventory))
checkpoint("Power-up loadout", loadout_ready)'''),
    md('''### Partner check

The Debugger points to:

1. The list variable.
2. The value added by `.append()`.
3. The condition that checks whether the value is in the list.'''),
    md('''## Level 3 — Coin Rush at 10:00

**Concept reminder:** A variable can be updated using its old value: `coins = coins + bonus`.

**Mission:** Use a `for` loop to add three team bonuses and reach at least `12` coins.

Before Run, the Predictor traces all three loop iterations and announces the final total.

**Tips**

- Trace the value after every update.
- Repair the three numbers in `team_bonuses`.
- Do not replace the loop with separate addition statements.
- The final value must make `coins >= 12` true.'''),
    code('''coins = 2
team_bonuses = [1, 1, 1]   # TODO: choose bonuses that reach 12 or more

print("Start:", coins)
for bonus in team_bonuses:
    coins = coins + bonus
    print("Added", bonus, "to the running total:", coins)

pipe_unlocked = coins >= 12
coin_loop_valid = integrity_check("Coin-loop integrity", [
    (type(team_bonuses) is list and len(team_bonuses) == 3, "Use a list containing exactly three bonuses."),
    (type(team_bonuses) is list and all(type(bonus) is int for bonus in team_bonuses), "Every bonus must be an integer."),
    (type(team_bonuses) is list and all(type(bonus) is int and 1 <= bonus <= 5 for bonus in team_bonuses), "Keep every bonus between 1 and 5."),
    (type(team_bonuses) is list and all(type(bonus) is int for bonus in team_bonuses) and coins == 2 + sum(team_bonuses), "coins must equal the start value plus every list bonus."),
])
pipe_unlocked = pipe_unlocked and coin_loop_valid
mario_level("LEVEL 3: COIN RUSH", "Loop to reach 12 coins", pipe_unlocked,
            "The loop finished below 12. Trace every iteration.",
            enemy="🕳️", coins=coins)
checkpoint("Coin total", pipe_unlocked)'''),
    md('''## Level 4 — Repair the If Condition

**Concept reminder:** An `if` statement runs its indented block only when the condition is `True`. `and` requires both sides to be true.

**Mission:** Open the castle door when Mario has at least 12 coins, has the key, **and** the Boo is not awake.

The starter uses `False`, so Mario always dies. Replace `False` with the correct condition.

**Tips**

- First comparison: `coins >= 12`
- Second condition: `has_key`
- Third condition: `not boo_awake`
- Join all three requirements with `and`.
- Your finished line begins with `if coins`.'''),
    code('''has_key = True
boo_awake = False

# TODO: replace False with all three requirements
if False:
    castle_open = True
else:
    castle_open = False

castle_valid = integrity_check("Castle-logic integrity", [
    (type(has_key) is bool and type(boo_awake) is bool, "Key and Boo states must stay Boolean."),
    (coins >= 12, "The earlier coin loop must still produce at least 12 coins."),
    (castle_open == (coins >= 12 and has_key and not boo_awake), "castle_open must match all three rules."),
])
castle_open = castle_open and castle_valid
mario_level("LEVEL 4: CASTLE DOOR", "Use coins, key, and Boo logic", castle_open,
            "The condition sent Mario into the lava. Repair the if line.",
            character="🏃", enemy="🔥", coins=coins)
checkpoint("Castle condition", castle_open)'''),
    md('''### Condition trace

The Reporter explains both sides separately:

- `coins >= 12` is ____.
- `has_key` is ____.
- `not boo_awake` is ____.
- All three joined with `and` become ____.'''),
    md('''## Final Boss — Bowser Condition

Pair with another team. One team controls Mario's attack. The other controls Bowser's defense.

**Mission:** Mario wins only when his attack is greater than Bowser's defense **and** he has a star.

The function is incomplete on purpose. Repair its `return` expression, predict the outcome, and run the battle.

**Tips**

- Compare `mario_attack` and `bowser_defense` with `>`.
- Check `team_has_star` in the same condition.
- Return one Boolean expression using `>` and `and`.
- If Mario still dies, print the three variable values and compare them.'''),
    code('''mario_attack = 5
bowser_defense = 3
team_has_star = True

def can_defeat_bowser(attack, defense, has_star):
    # TODO: replace False with the complete two-part condition
    return False

bowser_defeated = can_defeat_bowser(mario_attack, bowser_defense, team_has_star)
boss_logic_valid = integrity_check("Boss-function integrity", [
    (can_defeat_bowser(5, 3, True) is True, "A stronger attack with a star must win."),
    (can_defeat_bowser(3, 5, True) is False, "A weaker attack must lose even with a star."),
    (can_defeat_bowser(5, 3, False) is False, "A missing star must cause a loss."),
    (can_defeat_bowser(3, 3, True) is False, "Equal attack and defense must not satisfy >."),
])
bowser_defeated = bowser_defeated and boss_logic_valid

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
    md('''## Opening diagnostic — repair the round tracker

Before the walkthrough, repair one loop that must count rounds, total points, and count high-scoring rounds. Run it once first, then use the failed checks as clues.

**Rules:** keep one loop, do not type the final totals directly, and update all three variables inside the loop.'''),
    code('''round_scores = [4, 11, 7, 13]
rounds_played = 0
total_points = 0
high_rounds = 0

for score in round_scores:
    # TODO: count this round
    # TODO: add score to total_points
    # TODO: if score is at least 10, count a high round
    pass

integrity_check("Opening loop integrity", [
    (round_scores == [4, 11, 7, 13], "Do not change the starter scores."),
    (rounds_played == len(round_scores), "Count one round per list item."),
    (total_points == sum(round_scores), "Build the total from every score."),
    (high_rounds == 2, "Count only scores of 10 or more."),
])'''),
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
    md('''### Level 1 self-check

Your repaired list must contain exactly five enemies. The test should pass without changing the test itself.'''),
    code('''integrity_check("Roster integrity", [
    (type(enemies) is list and len(enemies) == 5, "Keep enemies as a five-item list."),
    (count == len(enemies), "The counter must match the list length."),
    (type(enemies) is list and len(set(enemies)) == 5, "Use five different enemy names."),
])'''),
    md('''## Level 2 — Accumulators build a total

An accumulator starts with a value and updates during every iteration. Trace `total` one line at a time.'''),
    code('''coin_values = [2, 5, 3]
total = 0

for coin in coin_values:
    print("Before:", total, "+", coin)
    total = total + coin
    print("After:", total)

checkpoint("Coin total", total == 10)'''),
    md('''### Trace, repair, and filter

Fill this in on paper: `0 → ___ → ___ → ___` for `[4, 1, 6]`.

Then repair the loop so `bonus_total` includes only scores of `5` or more.'''),
    code('''scores = [4, 1, 6]
total = 0
bonus_total = 0
for score in scores:
    total += score
    # TODO: if score is at least 5, add it to bonus_total

print("Team score:", total)
print("Bonus score:", bonus_total)
integrity_check("Accumulator integrity", [
    (scores == [4, 1, 6], "Do not change the starter scores."),
    (total == sum(scores), "total must include every score."),
    (bonus_total == 6, "bonus_total must include only scores of 5 or more."),
])'''),
    md('''## Level 3 — Build a new list

Start with an empty list. The loop creates and appends one new value per iteration.'''),
    code('''base_damage = [2, 4, 6, 9]
powered_damage = []

for damage in base_damage:
    # TODO: append double damage only when damage is 4 or more
    pass

print(powered_damage)
integrity_check("Power-list integrity", [
    (base_damage == [2, 4, 6, 9], "Do not change base_damage."),
    (powered_damage == [8, 12, 18], "Filter first, then double each accepted value."),
    (powered_damage is not base_damage, "Build a new list instead of reusing base_damage."),
])'''),
    md('''## Level 4 — While loops need an exit

Ask two questions: **What keeps the loop running? What changes so it stops?**'''),
    code('''energy = 3

while energy > 0:
    print("🏃 Energy:", energy)
    energy = energy - 1

print("REST")
checkpoint("While loop stops", energy == 0)'''),
    md('''### Repair challenge

This starter has two missing updates. Make the game end after four turns and collect one coin on every even-numbered turn.'''),
    code('''turns_left = 4
coins = 0

while turns_left > 0:
    print("Turn", turns_left)
    # TODO: add 1 coin when turns_left is even
    # TODO: subtract 1 from turns_left every iteration
    break  # remove this after adding the update

print("Game over with", coins, "coins")
integrity_check("While-loop integrity", [
    (turns_left == 0, "The changing condition must end at zero."),
    (coins == 2, "Only turns 4 and 2 should award coins."),
])'''),
    md('''## Boss challenge — Arcade scoreboard

Complete one loop that counts games, totals scores, counts bonus rounds, and stores winning scores in a new list.'''),
    code('''scores = [8, 12, 5, 15]
games_played = 0
total_score = 0
bonus_rounds = 0
winning_scores = []

for score in scores:
    # TODO: update games_played and total_score
    # TODO: scores of 10 or more update bonus_rounds and winning_scores
    pass

print("Games:", games_played)
print("Total:", total_score)
integrity_check("Loop-boss integrity", [
    (scores == [8, 12, 5, 15], "Do not change the boss input scores."),
    (games_played == len(scores), "Count every game exactly once."),
    (total_score == sum(scores), "Accumulate every score."),
    (bonus_rounds == 2, "Count the two scores of 10 or more."),
    (winning_scores == [12, 15], "Append qualifying scores in their original order."),
])'''),
    md('''## Loop mastery check

Point to the loop variable, collection, repeated block, accumulator, and stopping condition. Explain each without reading the definition.''')
])

write("module-3-power-up-functions.ipynb","Module 3: Power-Up Function Factory",[
    common_setup,
    md('''## Opening diagnostic — repair the power-up function

This function must approve a power-up only when it has uses remaining **and** its name is in the allowed list. Replace `False` with one Boolean expression. Do not change the checks.'''),
    code('''def can_equip(item, uses_left):
    allowed_items = ["Fire Flower", "Super Star", "Tanooki Suit"]
    if False:  # TODO: combine membership, comparison, and and
        return True
    return False

integrity_check("Power-up function integrity", [
    (can_equip("Fire Flower", 2) is True, "An allowed item with uses remaining must pass."),
    (can_equip("Fire Flower", 0) is False, "Zero remaining uses must fail."),
    (can_equip("Mystery Box", 3) is False, "An unknown item must fail."),
    (can_equip("Tanooki Suit", -1) is False, "Negative uses must fail."),
])'''),
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

Repair the returned player card so it contains the name, game, and score in that order.'''),
    code('''def player_card(name, game, score):
    # TODO: include game between name and score
    return [name, score]

maya_card = player_card("Maya", "Kart", 12)
devin_card = player_card("Devin", "Platformer", 18)
print(maya_card)
print(devin_card)
integrity_check("Parameter-card integrity", [
    (maya_card == ["Maya", "Kart", 12], "Return Maya's three arguments in order."),
    (devin_card == ["Devin", "Platformer", 18], "The function must work for different arguments."),
    (maya_card is not devin_card, "Each call must create its own result."),
])'''),
    md('''## Level 2 — Return sends a value back

`print()` shows a value. `return` gives a value back to the calling code so it can be saved or reused.'''),
    code('''def add_bonus(score, bonus):
    # A negative bonus is not allowed. Return the original score instead.
    if bonus < 0:
        return score
    new_score = score + bonus
    return new_score

final_score = add_bonus(10, 5)
protected_score = add_bonus(10, -5)
print("Final:", final_score, "Protected:", protected_score)
integrity_check("Bonus-function integrity", [
    (final_score == 15, "Positive bonuses must be added."),
    (protected_score == 10, "Negative bonuses must leave the score unchanged."),
    (add_bonus(0, 7) == 7, "Do not hard-code the first example."),
    (add_bonus(4, -1) == 4, "The guard must work with other scores."),
])'''),
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
    md('''## Level 3 — Functions can combine decisions

Repair the ranking rules. GOLD requires a score of at least 20 **and** a completed quest. SILVER requires at least 10.'''),
    code('''def rank_player(score, quest_complete):
    if False:  # TODO: replace False with the two-part GOLD condition
        return "GOLD"
    elif score >= 10:
        return "SILVER"
    else:
        return "BRONZE"

print(rank_player(8, True))
print(rank_player(14, False))
print(rank_player(25, True))
integrity_check("Rank-function integrity", [
    (rank_player(25, True) == "GOLD", "A high score plus a completed quest earns GOLD."),
    (rank_player(25, False) == "SILVER", "A missing quest blocks GOLD."),
    (rank_player(10, True) == "SILVER", "A score of 10 earns SILVER."),
    (rank_player(9, True) == "BRONZE", "A score below 10 earns BRONZE."),
])'''),
    md('''## Level 4 — Functions can contain loops

Trace `total` and `high_scores` after every score. The function returns two results.'''),
    code('''def score_report(scores):
    total = 0
    high_scores = []
    for score in scores:
        total += score
        # TODO: append scores of 10 or more to high_scores
    return total, high_scores

team_total, team_high_scores = score_report([4, 12, 6, 15])
print(team_total, team_high_scores)
second_total, second_high_scores = score_report([10, 2, 20])
integrity_check("Report-function integrity", [
    (team_total == 37 and team_high_scores == [12, 15], "Return the correct total and filtered list."),
    (second_total == 32 and second_high_scores == [10, 20], "Do not hard-code the first input list."),
    (team_high_scores is not second_high_scores, "Create a new result list for every call."),
])'''),
    md('''## Boss challenge — Battle report

Complete `average_score` and `best_score`. Then use all three functions to create the report.'''),
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

def best_score(scores):
    best = scores[0]
    for score in scores:
        # TODO: replace best when score is greater
        pass
    return best

battle_scores = [8, 12, 10]
average = average_score(battle_scores)
message = battle_message(average)
best = best_score(battle_scores)
print("Average:", average)
print("Best:", best)
print(message)

# Multiple cases catch hard-coded return values.
integrity_check("Function-boss integrity", [
    (average == 10 and best == 12 and message == "BOSS DEFEATED", "Complete the provided battle report."),
    (average_score([2, 4, 6]) == 4, "average_score must work for another list."),
    (best_score([3, 9, 5, 7]) == 9, "best_score must compare every item."),
    (battle_message(9) == "TRAIN AND RETRY", "A low average must not defeat the boss."),
])'''),
    md('''## Exit check

Draw arrows from argument → parameter → local variable → return value. Explain why a function with no `return` gives `None`.''')
])

print("Created Week 5 notebooks")
