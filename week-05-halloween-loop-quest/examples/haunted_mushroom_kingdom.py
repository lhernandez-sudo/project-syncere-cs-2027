"""Super Mario: Haunted Python Kingdom, a six-color foundations review.

This unofficial classroom fan game uses original terminal art and no external assets.
Run with Python 3.12 or newer.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Callable


RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"

COLORS = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]


def enable_windows_ansi() -> None:
    """Enable ANSI colors and UTF-8 art in modern Windows terminals."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if os.name == "nt":
        os.system("chcp 65001 > nul")
        os.system("")


def clear_screen() -> None:
    """Clear the terminal between scenes."""
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def color(text: str, shade: str) -> str:
    """Return text wrapped in one of the game's six ANSI colors."""
    return f"{shade}{text}{RESET}"


def pause(message: str = "Press Enter to continue...") -> None:
    """Wait until the player is ready."""
    input(color(message, CYAN))


def banner() -> None:
    """Display original retro terminal art."""
    art = r"""
              ██████████
          ████  ████  ████
        ██  ██  ████  ██  ██
        ██              ██
          ██████████████
             ██    ██
          ██████████████
        ██  ██  ██  ██  ██
        ██  ██████████  ██
          ██  ██  ██  ██

      SUPER MARIO: HAUNTED PYTHON KINGDOM
             A LOOP QUEST
"""
    for index, line in enumerate(art.splitlines()):
        print(color(line, COLORS[index % len(COLORS)]))


@dataclass
class Player:
    """Store the variables that change while the game runs."""

    name: str
    coins: int = 0
    lives: int = 3
    badges: list[str] = field(default_factory=list)


def show_status(player: Player) -> None:
    """Print current variable and list values."""
    print(
        color(
            f"PLAYER: {player.name}   COINS: {player.coins}   "
            f"LIVES: {player.lives}   BADGES: {len(player.badges)}/5",
            YELLOW,
        )
    )
    print(color("─" * 72, BLUE))


def ask_question(
    prompt: str,
    choices: dict[str, str],
    correct: str,
    explanation: str,
    reader: Callable[[str], str] = input,
) -> bool:
    """Ask a multiple-choice question and explain the result."""
    print(prompt)
    for key, answer in choices.items():
        print(f"  {color(key, CYAN)}. {answer}")

    while True:
        answer = reader(color("Your choice: ", CYAN)).strip().lower()
        if answer in choices:
            break
        print(color(f"Choose one of: {', '.join(choices)}", RED))

    if answer == correct:
        print(color("★ CORRECT! You found a power star.", GREEN))
        print(explanation)
        return True

    print(color(f"Not yet. The correct choice is {correct.upper()}.", MAGENTA))
    print(explanation)
    return False


def finish_level(player: Player, badge: str, correct: bool) -> None:
    """Update game variables after a completed level."""
    reward = 10 if correct else 5
    player.coins += reward
    player.badges.append(badge)
    print(color(f"LEVEL CLEAR: +{reward} coins and the {badge} badge!", YELLOW))
    pause()


def level_variables_and_lists(player: Player) -> None:
    """Level 1: review variables, lists, append, and len."""
    clear_screen()
    show_status(player)
    print(color("WORLD 1-1 — TOAD'S INVENTORY PIPE", GREEN))
    print("Toad gives Mario this inventory before he enters the pipe:\n")
    print(color('items = ["mushroom", "key"]', BLUE))
    print(color('items.append("flashlight")', BLUE))
    print(color("print(len(items))", BLUE))
    print()
    correct = ask_question(
        "What will the code print?",
        {"a": "2", "b": "3", "c": "flashlight"},
        "b",
        "A list stores Mario's items. append() adds one value, so len(items) is 3.",
    )
    finish_level(player, "LIST", correct)


def level_conditionals(player: Player) -> None:
    """Level 2: review if conditions and Boolean logic."""
    clear_screen()
    show_status(player)
    print(color("WORLD 2-1 — BOO'S HAUNTED HOUSE", MAGENTA))
    print("Mario reaches a Boo door controlled by two Boolean conditions:\n")
    print(color("has_key = True", BLUE))
    print(color("ghost_asleep = False", BLUE))
    print(color("if has_key and not ghost_asleep:", BLUE))
    print(color('    print("Enter carefully")', BLUE))
    print(color("else:", BLUE))
    print(color('    print("Door locked")', BLUE))
    print()
    correct = ask_question(
        "Which message prints?",
        {"a": "Enter carefully", "b": "Door locked", "c": "Nothing"},
        "a",
        "Mario has the key, and not False becomes True, so the if branch runs.",
    )
    finish_level(player, "LOGIC", correct)


def level_for_loop(player: Player) -> None:
    """Level 3: review for loops and accumulators."""
    clear_screen()
    show_status(player)
    print(color("WORLD 3-1 — SUPER MARIO COIN ROAD", YELLOW))
    print("Mario runs across the level and collects every coin value in a list:\n")
    print(color("coin_values = [2, 4, 6]", BLUE))
    print(color("total = 0", BLUE))
    print(color("for coin in coin_values:", BLUE))
    print(color("    total = total + coin", BLUE))
    print(color("print(total)", BLUE))
    print()
    print("Trace: 0 + 2 = 2, then 2 + 4 = 6, then 6 + 6 = ?")
    correct = ask_question(
        "What final value prints?",
        {"a": "6", "b": "10", "c": "12"},
        "c",
        "A for loop visits every item. total is an accumulator: 0 → 2 → 6 → 12.",
    )
    finish_level(player, "FOR LOOP", correct)


def level_while_loop(player: Player) -> None:
    """Level 4: use and review a while loop."""
    clear_screen()
    show_status(player)
    print(color("WORLD 4-1 — THE WARP PIPE MAZE", RED))
    print("This world really uses a while loop. Find warp pipe 3 to escape.")

    door = ""
    attempts = 0
    while door != "3":
        door = input(color("Choose warp pipe 1, 2, or 3: ", CYAN)).strip()
        attempts += 1
        if door == "3":
            print(color("Mario exits the pipe! The while condition is now False.", GREEN))
        elif door in {"1", "2"}:
            print(color("A Boo pops out and sends Mario back. Try again!", MAGENTA))
        else:
            print(color("That is not a warp pipe. The loop repeats.", RED))

    print(color(f"The loop ran {attempts} time(s).", YELLOW))
    correct = ask_question(
        "Why did the while loop stop?",
        {
            "a": "Python got tired",
            "b": 'door != "3" became False',
            "c": "while loops always run three times",
        },
        "b",
        "A while loop repeats while its condition is True. Choosing 3 made the condition False.",
    )
    finish_level(player, "WHILE LOOP", correct)


def spooky_power(base_power: int, moon_bonus: int) -> int:
    """Return a calculated power value for Level 5."""
    return base_power + moon_bonus


def level_functions(player: Player) -> None:
    """Level 5: review parameters, arguments, and return values."""
    clear_screen()
    show_status(player)
    print(color("WORLD 5-1 — BOWSER'S FUNCTION CASTLE", CYAN))
    print("Bowser's final machine contains this reusable function:\n")
    print(color("def spooky_power(base_power, moon_bonus):", BLUE))
    print(color("    return base_power + moon_bonus", BLUE))
    print()
    print(color("result = spooky_power(7, 5)", BLUE))
    print(color("print(result)", BLUE))
    print()
    correct = ask_question(
        "Which value is returned and printed?",
        {"a": "5", "b": "7", "c": "12"},
        "c",
        "7 and 5 are arguments. The parameters receive them, and return sends back 12.",
    )
    finish_level(player, "FUNCTION", correct)


def finale(player: Player) -> None:
    """Celebrate and connect the game code to the reviewed concepts."""
    clear_screen()
    banner()
    show_status(player)
    print(color("MARIO DEFEATED BOWSER'S BUGS AND SAVED PEACH!", GREEN))
    print()
    print("The game itself used every concept you reviewed:")
    print(color("  • variables stored coins, lives, and your name", CYAN))
    print(color("  • a list stored your badges", GREEN))
    print(color("  • if statements checked answers and doors", MAGENTA))
    print(color("  • for loops colored the opening art", YELLOW))
    print(color("  • a while loop repeated until you chose door 3", RED))
    print(color("  • functions organized each level", BLUE))
    print()
    print(color("Happy Halloween, Super Mario Python programmers!", YELLOW))


def run_game() -> None:
    """Run all five review levels in order."""
    enable_windows_ansi()
    clear_screen()
    banner()
    print("Bowser and his Boo crew scrambled the Mushroom Kingdom's Python code.")
    print("Clear five worlds so Mario can rescue Peach before midnight.\n")
    name = input(color("Player name or costume name: ", CYAN)).strip() or "Mario"
    player = Player(name=name)
    pause()

    levels = [
        level_variables_and_lists,
        level_conditionals,
        level_for_loop,
        level_while_loop,
        level_functions,
    ]
    for level in levels:
        level(player)

    finale(player)


def self_test() -> None:
    """Run fast checks without starting the interactive game."""
    player = Player("Test Player")
    assert player.coins == 0
    assert player.badges == []
    assert spooky_power(7, 5) == 12
    assert spooky_power(0, 0) == 0
    assert len(COLORS) == 6
    print("All Super Mario Haunted Python Kingdom self-tests passed.")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        run_game()
