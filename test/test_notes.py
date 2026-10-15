import unittest
from copy import deepcopy
from campusflow.notes import add_note


class TestNotes(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {"id": "T001", "status": "open", "notes": []}
        ]

    def test_add_note(self):
        note = add_note(self.tickets, "T001", "John", "Checking network")
        self.assertEqual(note["note_id"], "N001")

    def test_sequential_ids(self):
        add_note(self.tickets, "T001", "John", "First note")
        note = add_note(self.tickets, "T001", "Mary", "Second note")
        self.assertEqual(note["note_id"], "N002")

    def test_blank_author(self):
        before = deepcopy(self.tickets)
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", " ", "Checking network")
        self.assertEqual(self.tickets, before)

    def test_short_message(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "John", "Hi")

    def test_resolved_ticket(self):
        self.tickets[0]["status"] = "resolved"
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "John", "Checking network")

    def test_failed_attempt_keeps_next_id(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "John", "Hi")

        note = add_note(self.tickets, "T001", "John", "Valid message")
        self.assertEqual(note["note_id"], "N001")