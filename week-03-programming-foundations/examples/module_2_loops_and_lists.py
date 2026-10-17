"""Module 2 example: lists, for loops, while loops, and accumulators."""


def main() -> None:
    practice_scores = [6, 8, 7, 9]
    total = 0

    print("Practice sessions:")
    for session_number, score in enumerate(practice_scores, start=1):
        print(f"Session {session_number}: {score}")
        total = total + score

    average = total / len(practice_scores)
    print(f"Average score: {average:.1f}")

    countdown = 3
    while countdown > 0:
        print(f"Starting next challenge in {countdown}...")
        countdown = countdown - 1

    print("Go!")


if __name__ == "__main__":
    main()
