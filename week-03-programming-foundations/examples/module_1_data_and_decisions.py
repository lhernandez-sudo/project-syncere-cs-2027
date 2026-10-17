"""Module 1 example: input, variables, types, expressions, and decisions."""


def main() -> None:
    name = input("What is your name? ").strip()
    practice_minutes_text = input("How many minutes did you practice? ").strip()
    practice_minutes = int(practice_minutes_text)

    focus_bonus = 5
    output_score = practice_minutes + focus_bonus

    print(f"\n{name}, your output score is {output_score}.")

    if output_score >= 35:
        print("Strong session. Write down what helped you focus.")
    else:
        print("Good start. Try one more focused block.")


if __name__ == "__main__":
    main()
