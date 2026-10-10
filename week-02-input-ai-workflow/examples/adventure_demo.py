"""A small instructor demo for input, variables, and conditional logic."""


def main() -> None:
    """Run a short choice-based adventure."""
    name = input("What is your name? ").strip()
    print(f"Welcome to the Mars station, {name}!")

    choice = input("Do you inspect the LAB or the GARAGE? ").strip().lower()

    if choice == "lab":
        print("You discover a plant growing without sunlight.")
    elif choice == "garage":
        print("You repair the rover and unlock the next mission.")
    else:
        print("That location is not available yet. Try lab or garage.")


if __name__ == "__main__":
    main()

