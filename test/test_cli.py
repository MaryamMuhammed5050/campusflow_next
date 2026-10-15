import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from main import (
    handle_create,
    handle_view_ticket,
    handle_assign,
    handle_update_status,
    handle_add_note,
    handle_work_queue,
    show_ticket,
    display_menu,
)


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.tickets = []

    def test_create_ticket(self):
        inputs = [
            "Network failure",
            "Network",
            "high",
            "12"
        ]

        with patch("builtins.input", side_effect=inputs):
            with patch("main.save_tickets"):
                handle_create(self.tickets)

        self.assertEqual(len(self.tickets), 1)
        self.assertEqual(self.tickets[0]["id"], "T001")
        self.assertEqual(self.tickets[0]["priority"], "critical")

    def test_create_ticket_invalid_users(self):
        inputs = [
            "Network failure",
            "Network",
            "high",
            "abc"
        ]

        with patch("builtins.input", side_effect=inputs):
            with patch("main.save_tickets"):
                handle_create(self.tickets)

        self.assertEqual(self.tickets, [])

    def test_view_missing_ticket(self):
        with patch("builtins.input", return_value="T999"):
            with io.StringIO() as output:
                with redirect_stdout(output):
                    handle_view_ticket(self.tickets)

                self.assertIn("Ticket not found", output.getvalue())

    def test_assign_ticket(self):
        self.create_sample_ticket()

        inputs = ["T001", "Monday"]

        with patch("builtins.input", side_effect=inputs):
            with patch("main.save_tickets"):
                handle_assign(self.tickets)

        self.assertEqual(
            self.tickets[0]["assigned_to"],
            "Monday"
        )

    def test_update_status(self):
        self.create_sample_ticket()
        self.tickets[0]["assigned_to"] = "Monday"

        inputs = ["T001", "in_progress"]

        with patch("builtins.input", side_effect=inputs):
            with patch("main.save_tickets"):
                handle_update_status(self.tickets)

        self.assertEqual(
            self.tickets[0]["status"],
            "in_progress"
        )

    def test_add_note(self):
        self.create_sample_ticket()

        inputs = [
            "T001",
            "Monday",
            "Investigating the issue"
        ]

        with patch("builtins.input", side_effect=inputs):
            with patch("main.save_tickets"):
                handle_add_note(self.tickets)

        self.assertEqual(len(self.tickets[0]["notes"]), 1)
        self.assertEqual(
            self.tickets[0]["notes"][0]["note_id"],
            "N001"
        )

    def test_work_queue(self):
        self.create_sample_ticket()

        with io.StringIO() as output:
            with redirect_stdout(output):
                handle_work_queue(self.tickets)

            self.assertIn("T001", output.getvalue())

    def test_show_ticket(self):
        self.create_sample_ticket()

        with io.StringIO() as output:
            with redirect_stdout(output):
                show_ticket(self.tickets[0])

            self.assertIn("Network failure", output.getvalue())

    def test_menu_contains_notes(self):
        with io.StringIO() as output:
            with redirect_stdout(output):
                display_menu()

            self.assertIn("8. Add note", output.getvalue())

    def create_sample_ticket(self):
        from campusflow.tickets import create_ticket

        create_ticket(
            self.tickets,
            "Network failure",
            "Network",
            "high",
            12
        )


if __name__ == "__main__":
    unittest.main()