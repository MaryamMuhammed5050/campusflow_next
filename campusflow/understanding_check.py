QUESTIONS = [
    {
        "id": "Q1",
        "question": (
            "What should happen if an unassigned ticket is changed "
            "to in_progress?"
        ),
        "options": {
            "A": "The status changes successfully",
            "B": "The ticket is automatically assigned",
            "C": "The change is rejected",
            "D": "The ticket is resolved",
        },
        "answer": "C",
    },
    {
        "id": "Q2",
        "question": (
            "What resolution percentage should an empty ticket "
            "report display?"
        ),
        "options": {
            "A": "0%",
            "B": "50%",
            "C": "100%",
            "D": "Undefined",
        },
        "answer": "A",
    },
    {
        "id": "Q3",
        "question": (
            "When multiple search filters are supplied, how should "
            "they be combined?"
        ),
        "options": {
            "A": "OR logic",
            "B": "AND logic",
            "C": "Only the first filter is used",
            "D": "Only the last filter is used",
        },
        "answer": "B",
    },
    {
        "id": "Q4",
        "question": (
            "What should happen when a user tries to add a note "
            "to a resolved ticket?"
        ),
        "options": {
            "A": "The note is added",
            "B": "The ticket is deleted",
            "C": "The note is rejected",
            "D": "A new ticket is created",
        },
        "answer": "C",
    },
    {
        "id": "Q5",
        "question": (
            "What should happen if duplicate ticket IDs are found "
            "while loading JSON data?"
        ),
        "options": {
            "A": "The duplicates are ignored",
            "B": "The IDs are automatically changed",
            "C": "The invalid data is rejected",
            "D": "Both tickets are loaded",
        },
        "answer": "C",
    },
    {
        "id": "Q6",
        "question": (
            "During pull request review, what should happen if "
            "important negative tests are missing?"
        ),
        "options": {
            "A": "Merge immediately",
            "B": "Request the missing tests before approval",
            "C": "Delete the pull request",
            "D": "Ignore the missing tests",
        },
        "answer": "B",
    },
]


def get_valid_answer(prompt="Your answer: "):
    while True:
        answer = input(prompt).strip().upper()

        if answer in ("A", "B", "C", "D"):
            return answer

        print("Invalid choice. Please enter A, B, C, or D.")


def get_explanations():
    explanations = []

    print("\n=== EXPLAIN TWO ANSWERS ===")
    print("Choose two questions and briefly explain your answers.")

    while len(explanations) < 2:
        question_id = input(
            f"Question to explain ({len(explanations) + 1}/2, Q1-Q6): "
        ).strip().upper()

        if question_id not in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6"):
            print("Invalid question. Please enter Q1, Q2, Q3, Q4, Q5, or Q6.")
            continue

        if any(item["question_id"] == question_id for item in explanations):
            print("You already explained that question. Choose another.")
            continue

        explanation = input("Your explanation: ").strip()

        if not explanation:
            print("Explanation cannot be blank.")
            continue

        explanations.append({
            "question_id": question_id,
            "explanation": explanation,
        })

    return explanations


def run_understanding_check():
    score = 0

    print("\n=== ENGINEERING UNDERSTANDING CHECK ===")

    for question in QUESTIONS:
        print(f"\n{question['id']}. {question['question']}")

        for letter, option in question["options"].items():
            print(f"  {letter}. {option}")

        answer = get_valid_answer()

        if answer == question["answer"]:
            score += 1
            print("Correct.")
        else:
            print(
                f"Incorrect. Correct answer: "
                f"{question['answer']}."
            )

    print(f"\nFinal Score: {score}/6")

    explanations = get_explanations()

    print("\nUnderstanding check completed.")

    return {
        "score": score,
        "total": len(QUESTIONS),
        "explanations": explanations,
    }