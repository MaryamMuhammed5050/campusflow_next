import unittest
from copy import deepcopy
from campusflow.notes import add_note


class TestNotes(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {"id": "T001", "status": "open", "notes": []}
        ]

    def test_add_note(self):
        note = add_note(
            self.tickets, "T001", "Maryam", "Checking network"
        )
        self.assertEqual(note["author"], "Maryam")
        self.assertEqual(note["note_id"], "N001")

    def test_sequential_ids(self):
        add_note(self.tickets, "T001", "Maryam", "First note")
        note = add_note(self.tickets, "T001", "Ada", "Second note")

        self.assertEqual(note["note_id"], "N002")

    def test_highest_note_id(self):
        self.tickets[0]["notes"] = [
            {"note_id": "N001", "author": "Ada", "message": "First note"},
            {"note_id": "N003", "author": "Maryam", "message": "Third note"}
        ]

        note = add_note(
            self.tickets, "T001", "Grace", "Another update"
        )

        self.assertEqual(note["note_id"], "N004")

    def test_blank_author(self):
        before = deepcopy(self.tickets)

        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", " ", "Checking network")

        self.assertEqual(self.tickets, before)

    def test_short_message(self):
        before = deepcopy(self.tickets)

        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Ada", "Hi")

        self.assertEqual(self.tickets, before)

    def test_long_message(self):
        before = deepcopy(self.tickets)

        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Ada", "A" * 301)

        self.assertEqual(self.tickets, before)

    def test_resolved_ticket(self):
        self.tickets[0]["status"] = "resolved"
        before = deepcopy(self.tickets)

        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Ada", "Checking network")

        self.assertEqual(self.tickets, before)

    def test_missing_ticket(self):
        before = deepcopy(self.tickets)

        with self.assertRaises(ValueError):
            add_note(self.tickets, "T999", "Ada", "Checking network")

        self.assertEqual(self.tickets, before)

    def test_failed_attempt_keeps_next_id(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Ada", "Hi")

        note = add_note(
            self.tickets, "T001", "Grace", "Valid message"
        )

        self.assertEqual(note["note_id"], "N001")

    def test_in_progress_ticket(self):
        self.tickets[0]["status"] = "in_progress"

        note = add_note(
            self.tickets, "T001", "Grace", "Working on issue"
        )

        self.assertEqual(note["note_id"], "N001")

    def test_author_and_message_trimmed(self):
        note = add_note(
            self.tickets, "T001", "  Ada  ", "  Checking network  "
        )

        self.assertEqual(note["author"], "Ada")
        self.assertEqual(note["message"], "Checking network")

    def test_invalid_author_type(self):
        before = deepcopy(self.tickets)

        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", 123, "Checking network")

        self.assertEqual(self.tickets, before)

    def test_invalid_message_type(self):
        before = deepcopy(self.tickets)

        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Ada", 12345)

        self.assertEqual(self.tickets, before)