import unittest

from campusflow.workflow import assign_ticket


class TestAssignTicket(unittest.TestCase):

    def test_assignment_updates_correct_field(self):

        tickets = [
            {
                "id": "T001",
                "status": "open",
                "assigned_to": None
            }
        ]

        assign_ticket(tickets, "T001", "John")

        self.assertEqual(
            tickets[0]["assigned_to"],
            "John"
        )