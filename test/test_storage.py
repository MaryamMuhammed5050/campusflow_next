import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from campusflow.notes import add_note

from campusflow.storage import load_tickets, save_tickets, StorageError
from campusflow.tickets import create_ticket


def sample_ticket():
    return {
        "id": "T001",
        "title": "Network is down",
        "category": "Network",
        "urgency": "high",
        "affected_users": 12,
        "priority": "critical",
        "status": "open",
        "assigned_to": None
    }


class TestLoadTickets(unittest.TestCase):

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "missing.json"

            result = load_tickets(path)

            self.assertEqual(result, [])

    def test_loads_valid_tickets(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"
            tickets = [sample_ticket()]

            path.write_text(json.dumps(tickets), encoding="utf-8")

            result = load_tickets(path)

            self.assertEqual(result, tickets)

    def test_loads_empty_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"
            path.write_text("[]", encoding="utf-8")

            self.assertEqual(load_tickets(path), [])

    def test_corrupted_json_raises_storage_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"
            corrupted_text = '{"id": "T001", invalid JSON'

            path.write_text(corrupted_text, encoding="utf-8")

            with self.assertRaisesRegex(
                StorageError, "Ticket file is corrupted"
            ):
                load_tickets(path)

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                corrupted_text
            )

    def test_non_list_json_raises_storage_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            path.write_text(
                '{"id": "T001"}',
                encoding="utf-8"
            )

            with self.assertRaisesRegex(
                StorageError, "Ticket file has the wrong format"
            ):
                load_tickets(path)

    def test_non_dictionary_ticket_raises_storage_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            path.write_text(
                json.dumps(["not a ticket"]),
                encoding="utf-8"
            )

            with self.assertRaisesRegex(
                StorageError, "Ticket file has the wrong format"
            ):
                load_tickets(path)

    def test_missing_required_field_raises_storage_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            ticket = sample_ticket()
            del ticket["title"]

            path.write_text(
                json.dumps([ticket]),
                encoding="utf-8"
            )

            with self.assertRaisesRegex(
                StorageError, "A ticket is missing field:"
            ):
                load_tickets(path)

    def test_read_failure_raises_storage_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            path.write_text("[]", encoding="utf-8")

            with patch(
                "builtins.open",
                side_effect=PermissionError("Permission denied")
            ):
                with self.assertRaisesRegex(
                    StorageError, "Could not read the file"
                ):
                    load_tickets(path)

    def test_rejects_duplicate_ticket_ids(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            tickets = [
                sample_ticket(),
                sample_ticket()
            ]

            path.write_text(
                json.dumps(tickets),
                encoding="utf-8"
            )

            with self.assertRaisesRegex(
                StorageError, "Duplicate ticket ID"
            ):
                load_tickets(path)

    def test_rejects_invalid_priority(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            ticket = sample_ticket()
            ticket["priority"] = "low"

            path.write_text(
                json.dumps([ticket]),
                encoding="utf-8"
            )

            with self.assertRaisesRegex(
                StorageError, "Invalid ticket priority"
            ):
                load_tickets(path)

    def test_rejects_invalid_ticket_id(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            ticket = sample_ticket()
            ticket["id"] = "INVALID"

            path.write_text(
                json.dumps([ticket]),
                encoding="utf-8"
            )

            with self.assertRaisesRegex(
                StorageError, "Invalid ticket ID"
            ):
                load_tickets(path)

    def test_rejects_invalid_notes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            ticket = sample_ticket()
            ticket["notes"] = "invalid"

            path.write_text(
                json.dumps([ticket]),
                encoding="utf-8"
            )

            with self.assertRaisesRegex(
                StorageError, "Invalid notes format"
            ):
                load_tickets(path)

    def test_loads_old_ticket_without_notes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            ticket = sample_ticket()

            path.write_text(
                json.dumps([ticket]),
                encoding="utf-8"
            )

            result = load_tickets(path)

            self.assertEqual(result, [ticket])
            self.assertEqual(result[0].get("notes", []), [])

    def test_rejects_duplicate_note_ids(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            ticket = sample_ticket()

            ticket["notes"] = [
                {
                    "note_id": "N001",
                    "author": "Monday",
                    "message": "Checking the network"
                },
                {
                    "note_id": "N001",
                    "author": "Ada",
                    "message": "Investigating the issue"
                }
            ]

            path.write_text(
                json.dumps([ticket]),
                encoding="utf-8"
            )

            with self.assertRaisesRegex(
                StorageError, "Duplicate note ID"
            ):
                load_tickets(path)


class TestSaveTickets(unittest.TestCase):

    def test_saves_tickets_successfully(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"
            tickets = [sample_ticket()]

            save_tickets(tickets, path)

            saved_tickets = json.loads(
                path.read_text(encoding="utf-8")
            )

            self.assertEqual(saved_tickets, tickets)

    def test_creates_missing_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "data" / "tickets.json"

            save_tickets([sample_ticket()], path)

            self.assertTrue(path.exists())

            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                [sample_ticket()]
            )

    def test_saved_json_is_indented(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            save_tickets([sample_ticket()], path)

            text = path.read_text(encoding="utf-8")

            self.assertIn("\n", text)
            self.assertIn('    "id": "T001"', text)

    def test_replaces_existing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            path.write_text("[]", encoding="utf-8")

            tickets = [sample_ticket()]

            save_tickets(tickets, path)

            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")),
                tickets
            )

    def test_save_failure_raises_storage_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            ticket = sample_ticket()
            ticket["unexpected"] = {1, 2, 3}

            with self.assertRaisesRegex(
                StorageError, "Could not save tickets"
            ):
                save_tickets([ticket], path)

            self.assertFalse(path.exists())

    def test_temporary_file_is_removed_after_success(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"
            temp_path = path.with_name(path.name + ".tmp")

            save_tickets([sample_ticket()], path)

            self.assertTrue(path.exists())
            self.assertFalse(temp_path.exists())

    def test_saves_and_loads_notes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            ticket = sample_ticket()

            ticket["notes"] = [
                {
                    "note_id": "N001",
                    "author": "Monday",
                    "message": "Investigating the network"
                }
            ]

            save_tickets([ticket], path)

            loaded = load_tickets(path)

            self.assertEqual(loaded, [ticket])

            self.assertEqual(
                loaded[0]["notes"][0]["note_id"],
                "N001"
            )

    def test_invalid_data_does_not_overwrite_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            original = [sample_ticket()]

            save_tickets(original, path)

            invalid = [sample_ticket()]
            invalid[0]["affected_users"] = -5

            with self.assertRaises(StorageError):
                save_tickets(invalid, path)

            self.assertEqual(load_tickets(path), original)

    def test_ticket_id_continues_after_restart(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            tickets = []

            create_ticket(
                tickets,
                "WiFi issue",
                "Network",
                "high",
                10
            )

            create_ticket(
                tickets,
                "Broken laptop",
                "Hardware",
                "low",
                2
            )

            create_ticket(
                tickets,
                "Software error",
                "Software",
                "medium",
                5
            )

            self.assertEqual(len(tickets), 3)

            save_tickets(tickets, path)

            loaded_tickets = load_tickets(path)

            self.assertEqual(len(loaded_tickets), 3)

            new_ticket = create_ticket(
                loaded_tickets,
                "Printer not working",
                "Hardware",
                "low",
                1
            )

            self.assertEqual(new_ticket["id"], "T004")
            self.assertEqual(len(loaded_tickets), 4)

            save_tickets(loaded_tickets, path)

            restarted_tickets = load_tickets(path)

            self.assertEqual(len(restarted_tickets), 4)
            self.assertEqual(restarted_tickets[-1]["id"], "T004")


    def test_note_id_continues_after_restart(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tickets.json"

            tickets = [
                {
                    "id": "T001",
                    "title": "Network failure",
                    "category": "Network",
                    "urgency": "high",
                    "affected_users": 12,
                    "priority": "critical",
                    "status": "open",
                    "assigned_to": None,
                    "notes": [
                        {
                            "note_id": "N001",
                            "author": "Monday",
                            "message": "Initial investigation completed"
                        }
                    ]
                }
            ]

            save_tickets(tickets, path)
            loaded_tickets = load_tickets(path)

            note = add_note(
                loaded_tickets,
                "T001",
                "Monday",
                "Checking the router again"
            )

            self.assertEqual(note["note_id"], "N002")
            self.assertEqual(
                len(loaded_tickets[0]["notes"]),
                2
            )

if __name__ == "__main__":
    unittest.main()