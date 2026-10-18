import unittest
from unittest.mock import patch

from campusflow.understanding_check import (
    QUESTIONS,
    get_explanations,
    get_valid_answer,
    run_understanding_check,
)


class TestUnderstandingCheck(unittest.TestCase):

    def test_has_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)

    @patch("builtins.input", side_effect=["x", "7", "", "b"])
    def test_invalid_answer_retries(self, mock_input):
        answer = get_valid_answer()

        self.assertEqual(answer, "B")
        self.assertEqual(mock_input.call_count, 4)

    @patch("builtins.input", return_value="c")
    def test_answer_is_case_insensitive(self, mock_input):
        answer = get_valid_answer()

        self.assertEqual(answer, "C")

    @patch(
        "builtins.input",
        side_effect=[
            "Q1",
            "Because an unassigned ticket cannot start work.",
            "Q2",
            "An empty report has zero resolved tickets.",
        ],
    )
    def test_collects_two_explanations(self, mock_input):
        explanations = get_explanations()

        self.assertEqual(len(explanations), 2)
        self.assertEqual(explanations[0]["question_id"], "Q1")
        self.assertEqual(explanations[1]["question_id"], "Q2")

    @patch(
        "builtins.input",
        side_effect=[
            "Q1",
            "First explanation",
            "Q1",
            "Q2",
            "Second explanation",
        ],
    )
    def test_duplicate_explanation_question_retries(self, mock_input):
        explanations = get_explanations()

        self.assertEqual(len(explanations), 2)
        self.assertEqual(explanations[0]["question_id"], "Q1")
        self.assertEqual(explanations[1]["question_id"], "Q2")

    @patch(
        "builtins.input",
        side_effect=[
            "C", "A", "B", "C", "C", "B",
            "Q1", "First explanation",
            "Q2", "Second explanation",
        ],
    )
    def test_all_correct_answers_score_six(self, mock_input):
        result = run_understanding_check()

        self.assertEqual(result["score"], 6)
        self.assertEqual(result["total"], 6)
        self.assertEqual(len(result["explanations"]), 2)

    @patch(
        "builtins.input",
        side_effect=[
            "A", "B", "A", "A", "A", "A",
            "Q1", "First explanation",
            "Q2", "Second explanation",
        ],
    )
    def test_wrong_answers_score_zero(self, mock_input):
        result = run_understanding_check()

        self.assertEqual(result["score"], 0)


if __name__ == "__main__":
    unittest.main()