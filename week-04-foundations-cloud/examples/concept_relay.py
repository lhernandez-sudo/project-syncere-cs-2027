"""Week 4 review: trace data through decisions, loops, and functions."""


def calculate_average(scores: list[int]) -> float:
    """Return the arithmetic mean of a non-empty list of scores."""
    total = 0
    for score in scores:
        total = total + score
    return total / len(scores)


def describe_progress(average: float) -> str:
    """Return feedback selected from the average score."""
    if average >= 8:
        return "Strong foundation. Explain one idea to a classmate."
    if average >= 5:
        return "The foundation is growing. Practice one more example."
    return "Slow down and trace one concept with a partner."


def main() -> None:
    """Run the review example."""
    student_name = "Jordan"
    practice_scores = [4, 7, 8]
    average = calculate_average(practice_scores)
    message = describe_progress(average)

    print(f"{student_name}'s scores: {practice_scores}")
    print(f"Average: {average:.1f}")
    print(message)


if __name__ == "__main__":
    main()

