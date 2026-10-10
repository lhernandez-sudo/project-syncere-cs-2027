"""Week 2 student project: customize this text adventure."""


def main() -> None:
    """Run the adventure game."""
    player_name = input("What is your name? ").strip()
    print(f"Welcome, {player_name}!")
    print("You arrive at a locked technology lab after sunset.")

    first_choice = input("Do you check the DOOR or the WINDOW? ").strip().lower()

    if first_choice == "door":
        print("The keypad asks for a four-digit access code.")
        # TODO: Ask the player for a code and create at least two outcomes.
    elif first_choice == "window":
        print("You see a service robot holding a keycard.")
        # TODO: Give the player another meaningful choice.
    else:
        print("That choice is not available. Run the game and try again.")

    # TODO: Add one feature with ChatGPT assistance.
    # TODO: After peer testing, implement one requested improvement.


if __name__ == "__main__":
    main()

