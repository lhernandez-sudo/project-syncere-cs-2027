"""Build the self-guided Week 6 Google Colab notebooks."""

import json
from pathlib import Path

OUT = Path(__file__).parent
BASE = "https://colab.research.google.com/github/lhernandez-sudo/project-syncere-cs-2027/blob/main/week-06-dictionaries-classes-review/exercises"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [line + "\n" for line in text.strip().splitlines()]}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + "\n" for line in text.strip().splitlines()]}


def intro(name, title, subtitle):
    links = " · ".join([
        f"[Icebreaker]({BASE}/00-icebreaker-secret-identity.ipynb)",
        f"[Dictionaries]({BASE}/01-dictionary-arcade.ipynb)",
        f"[Classes]({BASE}/02-friendly-character-classes.ipynb)",
        f"[Final challenge]({BASE}/03-data-model-showdown.ipynb)",
    ])
    return md(f'''<div style="background:#071a33;color:white;padding:22px;border-radius:16px">
<h1>{title}</h1><p>{subtitle}</p></div>

[**Open this notebook in Google Colab**]({BASE}/{name})

### Save your Google Workspace copy

1. Choose **File → Save a copy in Drive**.
2. Rename it with your name and the notebook number.
3. Work only in the saved copy.

### Week 6 navigation

{links}

> Read every instruction and every failed check. Fix one issue at a time. Do not edit the check code.''')


SETUP = code('''def checkpoint(name, passed):
    icon = "✅" if passed else "🔁"
    print(f"{icon} {name}: {'CLEARED' if passed else 'REPAIR AND RUN AGAIN'}")
    return passed

def integrity_check(name, rules):
    failed = [message for passed, message in rules if not passed]
    checkpoint(name, not failed)
    for message in failed:
        print("   ↳", message)
    return not failed

print("🧪 Integrity checks loaded. Failed checks are clues, not punishments.")''')


def write(name, title, subtitle, cells):
    notebook = {
        "cells": [intro(name, title, subtitle), SETUP] + cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (OUT / name).write_text(json.dumps(notebook, indent=1), encoding="utf-8")


write("00-icebreaker-secret-identity.ipynb", "Icebreaker: Secret Identity Draft", "Team game • no programming lesson required", [
    md('''## Teams of 3 or 4

Choose Driver, Reader, Tracer, and Tester. With three students, Reader also serves as Tester.

This icebreaker uses dictionaries, but you do not need to understand them yet. Run each cell in order and follow the prompts.'''),
    code('''from IPython.display import HTML, display
import random

characters = [
    {"alias": "Pixel Phantom", "power": "invisibility", "snack": "hot chips", "weakness": "group projects"},
    {"alias": "Captain Compile", "power": "super speed", "snack": "pizza", "weakness": "missing colons"},
    {"alias": "DJ Debug", "power": "time rewind", "snack": "cookies", "weakness": "infinite loops"},
    {"alias": "The Boolean", "power": "truth vision", "snack": "fruit snacks", "weakness": "mixed signals"},
]

random.shuffle(characters)
display(HTML("""<div style='background:linear-gradient(135deg,#071a33,#6d28d9);color:white;padding:24px;border-radius:18px;text-align:center'><h2>🕵️ SECRET IDENTITY DRAFT</h2><p>One clue reader. One guess per team. No phones needed.</p></div>"""))
print("Character deck shuffled:", len(characters), "secret identities")'''),
    md('''## Round 1: clue battle

The Reader runs the next cell without showing the alias. The team has 30 seconds to invent a better superhero name from the clues. Share the funniest appropriate answer.'''),
    code('''secret = characters[0]
print("POWER:", secret["power"])
print("FAVORITE SNACK:", secret["snack"])
print("WEAKNESS:", secret["weakness"])
print("\\nTeam-created alias: ____________________")'''),
    code('''print("Official ridiculous alias:", secret["alias"])
print("Give your team's alias one point if the group prefers it.")'''),
    md('''## Round 2: build the team identity

Agree on one team alias, one harmless superpower, one snack, and one coding weakness. The Driver edits only the four values.'''),
    code('''team_identity = {
    "alias": "TODO",
    "power": "TODO",
    "snack": "TODO",
    "weakness": "TODO",
}

integrity_check("Team identity", [
    (type(team_identity) is dict, "Keep team_identity as a dictionary."),
    (set(team_identity) == {"alias", "power", "snack", "weakness"}, "Keep all four required keys."),
    (all(type(value) is str and value.strip() and value != "TODO" for value in team_identity.values()), "Replace every TODO with an appropriate answer."),
])
print("\\nTEAM CARD")
for label, value in team_identity.items():
    print(label.upper() + ":", value)'''),
    md('''## Finish

Each team reads its alias and weakness. Keep the team for Notebook 1, then rotate roles.'''),
])


write("01-dictionary-arcade.ipynb", "Notebook 1: Dictionary Arcade", "Keys, values, updates, loops, and practical records", [
    md('''## Why dictionaries?

A list answers **what position?** A dictionary answers **what label?**

```python
player = {"name": "Ari", "score": 12, "online": True}
```

The keys are `"name"`, `"score"`, and `"online"`. Each key points to one value. Dictionaries work well for profiles, settings, inventory counts, and records returned by web APIs.'''),
    md('''## Syntax rules

- Use braces: `{}`
- Separate each key from its value with a colon.
- Separate pairs with commas.
- String keys need quotes.
- Keys must be unique.

A syntax error prevents Python from reaching the integrity checks. Read the highlighted line, repair the punctuation, and rerun.'''),
    code('''player = {"name": "Ari", "score": 12, "online": True}
print(player["name"])
print(player["score"])

integrity_check("Working dictionary", [
    (type(player) is dict, "player must be a dictionary."),
    (player["name"] == "Ari", "The name key should store Ari."),
    (player["score"] == 12, "The score key should store 12."),
])'''),
    md('''## Challenge 1: repair a game inventory

Run the starter once. Then add the missing `"coins"` key, update potions to `3`, and keep every original item.'''),
    code('''inventory = {"keys": 1, "potions": 1, "map": True}

# TODO: update potions to 3
# TODO: add a coins key with value 25

integrity_check("Inventory syntax and structure", [
    (type(inventory) is dict, "inventory must remain a dictionary."),
    (set(inventory) == {"keys", "potions", "map", "coins"}, "Keep the original keys and add coins."),
    (inventory.get("potions") == 3, "Update potions with square-bracket assignment."),
    (inventory.get("coins") == 25, "Add 25 coins."),
    (inventory.get("map") is True, "Do not remove or change the map."),
])'''),
    md('''## Safe access with `.get()`

`inventory["shield"]` raises `KeyError` when the key is missing. `inventory.get("shield", 0)` returns the fallback value `0`. Use `.get()` for optional data.'''),
    code('''shield_count = inventory.get("shield", 0)
coin_count = inventory.get("coins", 0)
print("Shields:", shield_count)
print("Coins:", coin_count)
checkpoint("Safe optional access", shield_count == 0 and coin_count == 25)'''),
    md('''## Challenge 2: loop through key-value pairs

`.items()` gives the key and value together. Complete the loop so it totals only integer item counts. Remember that `bool` is technically related to `int`, so use `type(value) is int` here.'''),
    code('''total_items = 0

for item, value in inventory.items():
    # TODO: if the value's exact type is int, add it to total_items
    pass

integrity_check("Inventory loop", [
    (total_items == 29, "Add keys, potions, and coins. Do not count the Boolean map."),
    (inventory == {"keys": 1, "potions": 3, "map": True, "coins": 25}, "Do not change the dictionary to force the total."),
])'''),
    md('''## Use case: one event record

A dictionary keeps related facts together. Complete the student event record and write `event_summary(record)` so it works with multiple records.'''),
    code('''event = {
    "title": "Game Night",
    "spots": 20,
    "registered": 14,
    # TODO: add location with value "Lab A"
}

def event_summary(record):
    # TODO: return a sentence using title, location, and remaining spots
    return "TODO"

integrity_check("Event record", [
    (event.get("location") == "Lab A", "Add the location key."),
    (event_summary(event) == "Game Night in Lab A has 6 spots left", "Calculate remaining spots from the record."),
    (event_summary({"title": "Hack Day", "location": "Room 2", "spots": 10, "registered": 3}) == "Hack Day in Room 2 has 7 spots left", "Do not hard-code the first event."),
])'''),
    md('''## Dictionary boss: snack shop order

Complete the functions. The order dictionary maps an item name to its quantity. The price dictionary maps an item name to its price.'''),
    code('''prices = {"chips": 2, "juice": 3, "cookie": 1}
order = {"chips": 2, "juice": 1, "cookie": 3}

def order_total(order_data, price_data):
    total = 0
    # TODO: loop through order_data.items()
    # TODO: add quantity * matching price
    return total

def add_item(order_data, item, quantity):
    # TODO: add quantity to the current amount; use .get(item, 0)
    pass

add_item(order, "juice", 2)
add_item(order, "fruit", 1)

integrity_check("Order functions", [
    (order == {"chips": 2, "juice": 3, "cookie": 3, "fruit": 1}, "Update existing items and add new items."),
    (order_total({"chips": 2, "cookie": 3}, prices) == 7, "Multiply each quantity by its price."),
    (order_total({"juice": 2}, prices) == 6, "The function must work with a different order."),
])'''),
    md('''## Notebook 1 exit check

In a Markdown cell, explain when you would use square brackets and when you would use `.get()`. Then rotate team roles and take the first break.'''),
])


write("02-friendly-character-classes.ipynb", "Notebook 2: Friendly Character Classes", "Objects, attributes, methods, and independent state", [
    md('''## The idea

A class is a blueprint. An object is one thing created from that blueprint.

Use a simple class when a program manages several things that share the same kinds of data and actions. A game may create many players from one `Player` class.'''),
    md('''## Class syntax

```python
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
```

- `class Player:` begins the blueprint.
- `__init__` runs when Python creates an object.
- `self` means the current object.
- `self.name` and `self.score` are attributes.

Indentation matters. A syntax or indentation error must be repaired before checks can run.'''),
    code('''class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

mario = Player("Mario")
luigi = Player("Luigi")
mario.score = 5

integrity_check("Independent objects", [
    (isinstance(mario, Player) and isinstance(luigi, Player), "Create both objects from Player."),
    (mario is not luigi, "Each constructor call must create a different object."),
    (mario.score == 5 and luigi.score == 0, "Changing Mario must not change Luigi."),
])'''),
    md('''## Challenge 1: constructor attributes

Repair the constructor. Each character needs a name, role, health, and starting score.'''),
    code('''class Character:
    def __init__(self, name, role, health):
        self.name = name
        # TODO: store role
        # TODO: store health
        self.score = 0

hero = Character("Nova", "healer", 4)
tank = Character("Brick", "tank", 8)

integrity_check("Character constructor", [
    (hasattr(hero, "role") and hero.role == "healer", "Store the role argument on self."),
    (hasattr(hero, "health") and hero.health == 4, "Store health on each object."),
    (hasattr(tank, "health") and tank.health == 8, "Do not hard-code the first health value."),
    (hero.score == 0 and tank.score == 0, "Every new character starts at zero score."),
])'''),
    md('''## Methods are object actions

A method is a function inside a class. It reads or changes the current object's attributes through `self`.'''),
    code('''class Character:
    def __init__(self, name, role, health):
        self.name = name
        self.role = role
        self.health = health
        self.score = 0

    def add_score(self, points):
        # TODO: increase this object's score by points
        pass

    def take_damage(self, amount):
        # TODO: reduce health but stop at 0
        pass

hero = Character("Nova", "healer", 4)
tank = Character("Brick", "tank", 8)
hero.add_score(3)
hero.add_score(2)
hero.take_damage(10)
tank.take_damage(3)

integrity_check("Character methods", [
    (hero.score == 5, "add_score must use the points argument every time."),
    (hero.health == 0, "Health must stop at zero."),
    (tank.health == 5 and tank.score == 0, "Objects must keep independent state."),
])'''),
    md('''## Challenge 2: return useful information

Methods can return values. Complete `status()` without printing inside it.'''),
    code('''class Player:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def level_up(self):
        self.level += 1

    def status(self):
        # TODO: return "NAME is level NUMBER"
        return "TODO"

player_one = Player("Ari", 2)
player_two = Player("Sam", 5)
player_one.level_up()

integrity_check("Player status", [
    (player_one.status() == "Ari is level 3", "Use this object's name and updated level."),
    (player_two.status() == "Sam is level 5", "The method must work for another object."),
    (player_one.level == 3 and player_two.level == 5, "level_up must change only its receiver."),
])'''),
    md('''## Class boss: reusable power-ups

Complete `use()`. A power-up returns its effect while uses remain. After that it returns `"EMPTY"`. Uses must never become negative.'''),
    code('''class PowerUp:
    def __init__(self, name, effect, uses):
        self.name = name
        self.effect = effect
        self.uses = uses

    def use(self):
        # TODO: check uses, subtract one, and return the correct string
        return "EMPTY"

flower = PowerUp("Fire Flower", "SHOOT", 2)
star = PowerUp("Star", "INVINCIBLE", 1)
flower_results = [flower.use(), flower.use(), flower.use()]
star_results = [star.use(), star.use()]

integrity_check("PowerUp behavior", [
    (flower_results == ["SHOOT", "SHOOT", "EMPTY"], "Return the effect exactly twice."),
    (star_results == ["INVINCIBLE", "EMPTY"], "Use each object's own effect and uses."),
    (flower.uses == 0 and star.uses == 0, "Uses must stop at zero."),
])'''),
    md('''## When a class is unnecessary

Do not create a class for every small value. A dictionary may be simpler for one event record or one configuration. Classes become useful when many objects share behavior and each object needs independent state.'''),
])


write("03-data-model-showdown.ipynb", "Notebook 3: Data Model Showdown", "Choose a structure and combine dictionaries with objects", [
    md('''## Dictionary or class?

Use a **dictionary** for a labeled record when behavior is minimal. Use a **class** when many objects share methods and keep independent state. Real programs often use both.'''),
    code('''choices = {
    "one event record": "dictionary",
    "twenty game enemies that take damage": "class",
    "application settings": "dictionary",
    "bank accounts with deposit methods": "class",
}

for situation, choice in choices.items():
    print(situation, "→", choice)'''),
    md('''## Challenge 1: team profile dictionary

Complete the team record. Keep members as a list and project_ready as a Boolean.'''),
    code('''team = {
    "name": "Code Crew",
    "members": ["Ari", "Sam", "Maya"],
    # TODO: add project_ready with value False
}

# TODO: add "Devin" to the members list

integrity_check("Team dictionary", [
    (type(team) is dict, "team must be a dictionary."),
    (team.get("project_ready") is False, "project_ready must be the Boolean False."),
    (team.get("members") == ["Ari", "Sam", "Maya", "Devin"], "Append Devin without replacing the list."),
])'''),
    md('''## Challenge 2: player objects

Complete the methods. The roster will hold objects created from this class.'''),
    code('''class Player:
    def __init__(self, name, skill):
        self.name = name
        self.skill = skill
        self.points = 0

    def earn(self, amount):
        # TODO: add amount to this player's points
        pass

    def summary(self):
        # TODO: return "NAME: SKILL, POINTS points"
        return "TODO"

roster = [Player("Ari", "design"), Player("Sam", "debugging"), Player("Maya", "testing")]
roster[0].earn(4)
roster[1].earn(2)
roster[1].earn(3)

integrity_check("Player objects", [
    (roster[0].points == 4 and roster[1].points == 5 and roster[2].points == 0, "Each object must track its own points."),
    (roster[0].summary() == "Ari: design, 4 points", "Build the summary from attributes."),
    (Player("Devin", "coding").summary() == "Devin: coding, 0 points", "Do not hard-code a roster member."),
])'''),
    md('''## Final artifact: roster report

Complete the function. It receives the team dictionary and list of Player objects. It returns a new dictionary with the team name, member count, total points, and one summary per player.'''),
    code('''def build_roster_report(team_data, players):
    # TODO: calculate total points with a loop
    # TODO: build a list of player summaries
    # TODO: return a new dictionary with the four required keys
    return {}

report = build_roster_report(team, roster)
second_report = build_roster_report(
    {"name": "Test Team", "members": ["Zoe"], "project_ready": True},
    [Player("Zoe", "planning")],
)

integrity_check("Roster report", [
    (type(report) is dict, "Return a dictionary."),
    (set(report) == {"team", "member_count", "total_points", "players"}, "Return exactly the required keys."),
    (report.get("team") == "Code Crew" and report.get("member_count") == 4, "Read team facts from team_data."),
    (report.get("total_points") == 9, "Total points must come from the Player objects."),
    (report.get("players") == ["Ari: design, 4 points", "Sam: debugging, 5 points", "Maya: testing, 0 points"], "Use each object's summary method."),
    (second_report == {"team": "Test Team", "member_count": 1, "total_points": 0, "players": ["Zoe: planning, 0 points"]}, "The function must work with different data."),
])

print(report)'''),
    md('''## Peer test

Exchange notebooks with a partner. The reviewer runs the final two cells, changes only a player name in a new test object, and confirms that `summary()` uses the new value. Add a Markdown note describing one successful design choice and one repaired issue.'''),
    md('''## Exit ticket

Answer in a Markdown cell:

1. Why is the team profile a dictionary?
2. Why are roster members objects?
3. Which structure might appear in your capstone?
4. What failed check helped you most today?'''),
])


print("Created Week 6 notebooks")
