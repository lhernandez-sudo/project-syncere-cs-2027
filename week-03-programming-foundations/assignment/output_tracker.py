"""Week 3 integrated challenge: Engineering Output Tracker.

The starter is runnable. Complete the TODO tasks without removing working code.
"""


def collect_scores() -> list[int]:
    """Collect three practice scores from the user."""
    scores: list[int] = []
    for session_number in range(1, 4):
        score = int(input(f"Score for session {session_number} (0-10): "))
        scores.append(score)
    return scores


def calculate_average(scores: list[int]) -> float:
    """Return the average of the supplied scores."""
    # TODO 1: Replace this placeholder with a loop that calculates the total.
    total = sum(scores)
    return total / len(scores)


def build_message(average: float) -> str:
    """Return feedback based on the average score."""
    # TODO 2: Add at least one more useful decision branch.
    if average >= 7:
        return "Your foundation is growing. Keep practicing deliberately."
    return "Choose one concept and give it another focused attempt."


def main() -> None:
    """Run the Engineering Output Tracker."""
    name = input("Engineer name: ").strip()
    scores = collect_scores()
    average = calculate_average(scores)
    message = build_message(average)

    print(f"\n{name}, your average practice score is {average:.1f}.")
    print(message)

    # TODO 3: Add one output that uses the scores list.


if __name__ == "__main__":
    main()
