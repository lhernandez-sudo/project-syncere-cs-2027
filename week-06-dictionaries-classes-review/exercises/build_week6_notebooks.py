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
        f"[Tech investigation]({BASE}/04-tech-controversy-investigation.ipynb)",
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


write("00-icebreaker-secret-identity.ipynb", "Icebreaker: Secret Identity Generator", "Individual, private, and low-pressure", [
    md('''## Make your own ridiculous coding character

Work independently. You do not have to present or share anything. This icebreaker uses a dictionary, but you do not need to understand dictionaries yet.

Run each cell in order. Reroll until you get a combination you like, then customize it.'''),
    code('''from IPython.display import HTML, display
import random

adjectives = ["Turbo", "Pixel", "Midnight", "Glitchy", "Cosmic", "Sneaky"]
roles = ["Debugger", "Wizard", "Phantom", "Racer", "Inventor", "Ninja"]
powers = ["time rewind", "instant debugging", "super speed", "invisibility", "perfect Wi-Fi"]
snacks = ["hot chips", "pizza", "cookies", "fruit snacks", "tacos"]
weaknesses = ["missing colons", "infinite loops", "low battery", "mystery errors", "Monday mornings"]

display(HTML("""<div style='background:linear-gradient(135deg,#071a33,#6d28d9);color:white;padding:24px;border-radius:18px;text-align:center'><h2>🕵️ SECRET IDENTITY GENERATOR</h2><p>Your character. Your choices. Sharing is optional.</p></div>"""))'''),
    md('''## Step 1: generate a draft

Run the next cell as many times as you want. Each run creates a new combination.'''),
    code('''draft_identity = {
    "alias": random.choice(adjectives) + " " + random.choice(roles),
    "power": random.choice(powers),
    "snack": random.choice(snacks),
    "weakness": random.choice(weaknesses),
}

print("🎲 YOUR RANDOM DRAFT")
for label, value in draft_identity.items():
    print(label.upper() + ":", value)'''),
    md('''## Step 2: customize your identity

Copy ideas from the draft or invent appropriate answers. Edit only the four values.'''),
    code('''my_identity = {
    "alias": "TODO",
    "power": "TODO",
    "snack": "TODO",
    "weakness": "TODO",
}

integrity_check("My identity", [
    (type(my_identity) is dict, "Keep my_identity as a dictionary."),
    (set(my_identity) == {"alias", "power", "snack", "weakness"}, "Keep all four required keys."),
    (all(type(value) is str and value.strip() and value != "TODO" for value in my_identity.values()), "Replace every TODO with an appropriate answer."),
])
print("\\n✨ SECRET IDENTITY CARD")
for label, value in my_identity.items():
    print(label.upper() + ":", value)'''),
    md('''## Finish

Save the notebook in Drive. If you want, show your alias to one person nearby. Sharing is optional. Then open Notebook 1.'''),
])


write("01-dictionary-arcade.ipynb", "Notebook 1: Dictionary Arcade", "Keys, values, updates, loops, and practical records", [
    md('''## Start here: a dictionary is a labeled container

You have not learned dictionaries before. That is expected.

A list stores values by position. A dictionary stores values under labels called **keys**. Think of a game profile where `"name"` labels the player's name and `"score"` labels the score.

```python
player = {"name": "Ari", "score": 12, "online": True}
```

The colon means **this key points to this value**. Run the next cell without changing it.'''),
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
    md('''## Practice A: read one value

Square brackets select a value using its key. Follow the pattern:

```python
player["name"]
```

Replace only `TODO` below.'''),
    code('''favorite_game = {
    "title": "Minecraft",
    "players": 4,
    "online": True,
}

game_title = favorite_game["TODO"]

integrity_check("Read one value", [
    (game_title == "Minecraft", "Use the title key inside the square brackets."),
])'''),
    md('''## Practice B: change and add values

Use the same square-bracket pattern for both actions:

```python
profile["score"] = 20      # change an existing value
profile["city"] = "Miami" # add a new key and value
```

Complete the two lines below.'''),
    code('''practice_profile = {"name": "Kai", "score": 5}

# Change score to 10
practice_profile["TODO"] = 10

# Add a snack key with the value "chips"
practice_profile["TODO"] = "chips"

integrity_check("Change and add", [
    (practice_profile.get("score") == 10, "Use score as the first key."),
    (practice_profile.get("snack") == "chips", "Use snack as the second key."),
    (practice_profile.get("name") == "Kai", "Keep the original name."),
])'''),
    md('''## Challenge 1: repair a game inventory

Run the starter once. Then add the missing `"coins"` key, update potions to `3`, and keep every original item.

**Hint:** copy the pattern from Practice B. You need two assignment lines.'''),
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

Sometimes a key might be missing. `inventory["shield"]` would stop with a `KeyError`. `inventory.get("shield", 0)` safely returns the backup value `0`.

Read `.get("shield", 0)` as: **get shield, but use 0 if shield is missing**.'''),
    code('''shield_count = inventory.get("shield", 0)
coin_count = inventory.get("coins", 0)
print("Shields:", shield_count)
print("Coins:", coin_count)
checkpoint("Safe optional access", shield_count == 0 and coin_count == 25)'''),
    md('''## Practice C: see a dictionary loop

The `.items()` method gives one key and one value on each loop. Run this example and trace the output.'''),
    code('''demo_inventory = {"keys": 1, "coins": 5}

for item, amount in demo_inventory.items():
    print(item, "has value", amount)'''),
    md('''## Challenge 2: loop through key-value pairs

Complete one line inside the loop. If the value is an integer, add it to `total_items`.

**Hint:** the missing line follows this pattern: `total = total + value`. Keep it indented under the `if`.'''),
    code('''total_items = 0

for item, value in inventory.items():
    if type(value) is int:
        # TODO: add value to total_items
        pass

integrity_check("Inventory loop", [
    (total_items == 29, "Add keys, potions, and coins. Do not count the Boolean map."),
    (inventory == {"keys": 1, "potions": 3, "map": True, "coins": 25}, "Do not change the dictionary to force the total."),
])'''),
    md('''## Use case: one event record

A dictionary keeps related facts together. Complete the student event record and function.

**Hint 1:** add `"location": "Lab A"` inside the dictionary.

**Hint 2:** calculate `remaining = record["spots"] - record["registered"]`, then build the sentence from the labeled values.'''),
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

Complete the functions. The order dictionary maps an item name to its quantity. The price dictionary maps an item name to its price.

Do this only after the earlier checks pass. Trace one item by hand before writing the loop. If time is short, stop here and save your notebook.'''),
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

In a Markdown cell, explain when you would use square brackets and when you would use `.get()`. Then take the first break.'''),
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
    md('''## Final self-test

Create one new test object with a different player name and points. Run `summary()` and confirm that it uses your new values. Add a Markdown note describing one successful design choice and one repaired issue. If you want help after trying once, compare the result with a neighbor.'''),
    md('''## Exit ticket

Answer in a Markdown cell:

1. Why is the team profile a dictionary?
2. Why are roster members objects?
3. Which structure might appear in your capstone?
4. What failed check helped you most today?'''),
])


write("04-tech-controversy-investigation.ipynb", "Tech Investigation: What Happens Behind the Screen?", "Small-group research, evidence, and discussion", [
    md('''## The goal

Technology companies make products that many people use every day. They also make business decisions about advertising, subscriptions, privacy, competition, and safety.

In a group of **2 or 3**, investigate one controversy. Your job is not to attack or defend a company. Your job is to understand:

1. How the product makes money.
2. What the government, consumers, or creators challenged.
3. What the company or opposing side says.
4. What evidence is established and what remains an allegation or open question.'''),
    md('''## Words that matter

- **Allegation:** a claim that has not yet been proven in court.
- **Lawsuit or complaint:** a legal case presenting one side's claims.
- **Ruling:** a court's decision on a legal question.
- **Settlement:** the parties resolve a case without completing a trial. A settlement does not always include an admission of wrongdoing.
- **Business model:** how a company earns revenue.
- **Dark pattern:** a design choice that pushes users toward a decision they may not intend.

Use these words accurately when you report.'''),
    md('''## Topic 1: TikTok, advertising, and children's privacy

**Behind the screen:** TikTok offers advertising tools that let businesses reach audiences. Like other social platforms, attention and user activity make advertising valuable.

**Controversy:** The U.S. Department of Justice sued TikTok and ByteDance in 2024 over alleged violations of children's privacy law. In August 2026, the parties reached a $400 million settlement. The Justice Department stated that the resolved claims were allegations and that the settlement included no determination of liability.

**Read this first:**

- [Associated Press: TikTok reaches a $400 million children's privacy settlement](https://apnews.com/article/7d92b65fa23968b8ce13ea3b5c52e7a4)

**Optional primary sources:**

- [Justice Department announcement of the 2024 complaint](https://www.justice.gov/archives/opa/pr/justice-department-sues-tiktok-and-parent-company-bytedance-widespread-violations-childrens)
- [Justice Department announcement of the 2026 settlement](https://www.justice.gov/opa/pr/justice-department-secures-400m-settlement-tiktok-and-bytedance-resolve-childrens-privacy)

**Question:** What responsibility should a platform have when young users enter an incorrect age?'''),
    md('''## Topic 2: Google Search, advertising, and competition

**Behind the screen:** Alphabet says Google Services earns revenue primarily from advertising, along with subscriptions, app sales, and devices.

**Controversy:** A federal court concluded in 2024 that Google unlawfully maintained a monopoly in general search services and search advertising. In 2025, the court restricted certain exclusive distribution agreements and required access to some search data and services for competitors.

**Read this first:**

- [PBS NewsHour and Associated Press: Court rules Google's search dominance is an antitrust violation](https://www.pbs.org/newshour/nation/court-rules-googles-search-engine-dominance-is-antitrust-violation-and-illegal)

**Optional primary and company sources:**

- [Alphabet explanation of Google Services revenue](https://abc.xyz/investor/faqs-and-general-information/)
- [Justice Department summary of the search remedies](https://www.justice.gov/opa/pr/department-justice-wins-significant-remedies-against-google)
- [Google's Search case resource center and company position](https://blog.google/competition/search-trial-resource-center/)

**Question:** When does paying to become the default search engine become unfair to competitors or users?'''),
    md('''## Topic 3: Instagram, advertising, and youth well-being

**Behind the screen:** Meta earns most of its revenue by showing advertisements across products such as Facebook and Instagram.

**Controversy:** A bipartisan group of state attorneys general sued Meta in 2023. Their complaint alleges that Meta designed features that contributed to harms experienced by young users and misrepresented some safety practices. These are legal allegations, not a final ruling.

**Read this first:**

- [Associated Press: States sue Meta over claims involving young users](https://apnews.com/article/17858802d76143d358e38ee15150dc94)

**Optional primary and company sources:**

- [Meta investor financial information](https://investor.atmeta.com/financials/)
- [New York Attorney General summary of the multistate lawsuit](https://ag.ny.gov/press-release/2023/attorney-general-james-and-multistate-coalition-sue-meta-harming-youth)
- [Meta's response about teen safety and the lawsuits](https://about.fb.com/news/2026/01/metas-record-protecting-teens-supporting-parents/)

**Question:** How should a social platform balance engagement, advertising revenue, and the well-being of younger users?'''),
    md('''## Topic 4: Amazon Prime and dark patterns

**Behind the screen:** Prime uses a recurring subscription. Amazon benefits when people join and remain subscribed.

**Controversy:** The Federal Trade Commission alleged that Amazon enrolled some consumers without clear consent and made cancellation unnecessarily difficult through dark patterns. Amazon reached a $2.5 billion settlement in 2025.

**Read this first:**

- [Associated Press: Amazon's $2.5 billion Prime settlement](https://apnews.com/article/a3aa849de1279e3675a162ec6815de84)

**Optional primary sources:**

- [FTC case summary and timeline](https://www.ftc.gov/legal-library/browse/cases-proceedings/2123050-amazoncom-inc-rosca-ftc-v)
- [FTC consumer explanation of the Prime case](https://consumer.ftc.gov/consumer-alerts/2023/06/were-you-charged-amazon-prime-without-your-permission)

**Question:** Which design choices help users make an informed choice, and which ones manipulate them?'''),
    md('''## Topic 5: Apple, the App Store, and control of the iPhone

**Behind the screen:** Apple earns money from hardware, subscriptions, and fees connected to apps and digital purchases.

**Controversy:** The Justice Department and multiple states sued Apple in 2024. The complaint alleges that Apple used restrictions on apps, messaging, wallets, watches, and cloud services to protect monopoly power. These claims are allegations in an ongoing legal case unless a source states otherwise.

**Read this first:**

- [Associated Press: Justice Department sues Apple over the smartphone market](https://apnews.com/article/822d7e8f5cf53a2636795fcc33ee1fc3)

**Optional primary and company sources:**

- [Justice Department summary of the Apple lawsuit](https://www.justice.gov/archives/opa/pr/justice-department-sues-apple-monopolizing-smartphone-markets)
- [Justice Department Apple case documents](https://www.justice.gov/atr/case/us-and-plaintiff-states-v-apple-inc)
- [Apple's explanation of App Store changes and developer policies](https://www.apple.com/newsroom/2021/08/apple-us-developers-agree-to-app-store-updates/)

**Question:** When does controlling a device protect users, and when does it limit competition?'''),
    md('''## Topic 6: Generative AI, training data, and creators

**Behind the screen:** Generative AI companies sell subscriptions, developer access, and business services. Their systems learn patterns from large collections of data.

**Controversy:** Writers, artists, publishers, and technology companies disagree about when copyrighted works may be used to train AI and what permission or payment should be required. The U.S. Copyright Office continues to study AI training and copyright policy.

**Read this first:**

- [PBS NewsHour and Associated Press: AI company settlement with book authors](https://www.pbs.org/newshour/nation/anthropic-to-pay-authors-1-5b-in-landmark-settlement-over-pirated-chatbot-training-material)

**Optional primary sources:**

- [U.S. Copyright Office artificial intelligence study](https://copyright.gov/ai/)
- [Copyright Office report on AI-generated outputs](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf)

**Question:** What would a fair relationship between AI developers and human creators look like?'''),
    md('''## Research organizer

Create a new Markdown cell under this one and answer together.

### Our topic

Company or technology:

### How it makes money

Explain in 2 or 3 sentences.

### What happened

Write a short timeline. Label each item as an **allegation**, **ruling**, or **settlement**.

### Who is affected

Name at least two groups of people and explain the possible impact on each.

### Evidence

Record two facts with links. Use at least one government, court, or company source.

### Our judgment

What should the company, government, or users do next? Explain one tradeoff or disagreement.'''),
    md('''## Two-minute share-out

Every group prepares four parts:

1. Name the product and explain how it makes money.
2. Explain the controversy without treating an allegation as a proven fact.
3. Share the strongest evidence you found.
4. Ask the class one discussion question.

You may divide the speaking or choose one reporter. No one must share personal experiences or account information.'''),
    md('''## Individual exit ticket

Answer privately in a Markdown cell:

1. Which business model surprised you most?
2. What is one fact you can now verify with a reliable source?
3. What question do you still have?
4. What should software engineers consider besides whether a product works?'''),
])


print("Created Week 6 notebooks")
