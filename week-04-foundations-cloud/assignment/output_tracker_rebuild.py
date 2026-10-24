"""Week 4 project: rebuild the Engineering Output Tracker.

The starter runs. Replace the marked placeholders without removing working code.
"""


def collect_scores() -> list[int]:
    """Collect and return three integer practice scores."""
    scores: list[int] = []
    for session_number in range(1, 4):
        score = int(input(f"Score for session {session_number} (0-10): "))
        scores.append(score)
    return scores


def calculate_average(scores: list[int]) -> float:
    """Return the average of the supplied scores."""
    # TODO 1: Use a loop and accumulator instead of sum().
    total = sum(scores)
    return total / len(scores)


def build_message(average: float) -> str:
    """Return feedback selected from the average."""
    # TODO 2: Add a middle branch for averages from 5 through 7.9.
    if average >= 8:
        return "Strong foundation. Explain one concept to someone else."
    return "Choose one concept and trace another example."


def main() -> None:
    """Run the tracker."""
    name = input("Engineer name: ").strip()
    scores = collect_scores()
    average = calculate_average(scores)
    message = build_message(average)

    print(f"\n{name}, your scores were {scores}.")
    print(f"Your average was {average:.1f}.")
    print(message)

    # TODO 3: Print the highest or lowest score from the list.


if __name__ == "__main__":
    main()

