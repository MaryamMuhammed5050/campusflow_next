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

    def test_assignment_rejects_blank_staff_name(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", " ")

    def test_assignment_rejects_unknown_ticket(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "John")

    def test_update_status(self):
        assign_ticket(self.tickets, "T001", "John")
        update_status(self.tickets, "T001", "in_progress")

        self.assertEqual(
            self.tickets[0]["status"],
            "in_progress"
        )

    def test_unassigned_ticket_cannot_be_in_progress(self):
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "in_progress")

        self.assertEqual(
            self.tickets[0]["status"],
            "open"
        )

    def test_resolved_ticket_cannot_be_modified(self):
        assign_ticket(self.tickets, "T001", "John")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "in_progress")

        self.assertEqual(
            self.tickets[0]["status"],
            "resolved"
        )

    def test_reopen_resolved_ticket(self):
        assign_ticket(self.tickets, "T001", "John")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")
        update_status(self.tickets, "T001", "open")

        self.assertEqual(
            self.tickets[0]["status"],
            "open"
        )

    def test_work_queue_sorts_by_priority(self):
        tickets = [
            {
                "id": "T001",
                "status": "open",
                "assigned_to": None,
                "priority": "low"
            },
            {
                "id": "T002",
                "status": "open",
                "assigned_to": None,
                "priority": "critical"
            },
            {
                "id": "T003",
                "status": "in_progress",
                "assigned_to": "John",
                "priority": "high"
            }
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T003", "T001"]
        )

    def test_work_queue_excludes_resolved_tickets(self):
        tickets = [
            {
                "id": "T001",
                "status": "open",
                "assigned_to": None,
                "priority": "high"
            },
            {
                "id": "T002",
                "status": "resolved",
                "assigned_to": "John",
                "priority": "critical"
            }
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T001"]
        )

    def test_same_priority_tickets_keep_original_order(self):
        tickets = [
            {
                "id": "T001",
                "status": "open",
                "assigned_to": None,
                "priority": "high"
            },
            {
                "id": "T002",
                "status": "open",
                "assigned_to": None,
                "priority": "high"
            }
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T001", "T002"]
        )


if __name__ == "__main__":
    unittest.main()