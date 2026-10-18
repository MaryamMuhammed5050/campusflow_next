import unittest

from campusflow.workflow import assign_ticket, update_status, get_work_queue


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "assigned_to": None,
                "priority": "high"
            }
        ]

    def test_assignment(self):
        assign_ticket(self.tickets, "T001", "John")

        self.assertEqual(
            self.tickets[0]["assigned_to"],
            "John"
        )

    def test_unassigned_ticket_cannot_start(self):
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "in_progress")

        self.assertEqual(self.tickets[0]["status"], "open")

    def test_assigned_ticket_can_start(self):
        assign_ticket(self.tickets, "T001", "John")

        update_status(self.tickets, "T001", "in_progress")

        self.assertEqual(
            self.tickets[0]["status"],
            "in_progress"
        )

    def test_resolved_ticket_cannot_be_assigned(self):
        self.tickets[0]["status"] = "resolved"

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "John")

        self.assertIsNone(self.tickets[0]["assigned_to"])

    def test_work_queue_contains_unresolved_tickets(self):
        self.tickets.append({
            "id": "T002",
            "status": "in_progress",
            "assigned_to": "John",
            "priority": "critical"
        })

        self.tickets.append({
            "id": "T003",
            "status": "resolved",
            "assigned_to": "Mary",
            "priority": "critical"
        })

        queue = get_work_queue(self.tickets)

        self.assertEqual(len(queue), 2)
        self.assertEqual(queue[0]["id"], "T001")
        self.assertEqual(queue[1]["id"], "T002")