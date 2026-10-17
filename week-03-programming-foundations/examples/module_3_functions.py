"""Module 3 example: parameters, return values, and decomposition."""


def calculate_average(scores: list[int]) -> float:
    """Return the arithmetic mean of a non-empty list of scores."""
    total = 0
    for score in scores:
        total = total + score
    return total / len(scores)


def describe_average(average: float) -> str:
    """Return feedback for an average practice score."""
    if average >= 8:
        return "Your foundation is getting stronger."
    if average >= 5:
        return "You are building consistency."
    return "Choose one small skill and practice it again."


def main() -> None:
    practice_scores = [6, 8, 7, 9]
    average = calculate_average(practice_scores)
    message = describe_average(average)

    print(f"Average score: {average:.1f}")
    print(message)


if __name__ == "__main__":
    main()
