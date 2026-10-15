import json
import re
from pathlib import Path

from campusflow.tickets import (
    check_title,
    check_category,
    check_urgency,
    check_affected_users,
    calculate_priority,
)

DEFAULT_PATH = "data/tickets.json"


class StorageError(Exception):
    pass


def validate_tickets(tickets):
    if not isinstance(tickets, list):
        raise StorageError("Ticket file has the wrong format")

    required_fields = {
        "id",
        "title",
        "category",
        "urgency",
        "affected_users",
        "priority",
        "status",
        "assigned_to"
    }

    seen_ids = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise StorageError("Ticket file has the wrong format")

        for field in required_fields:
            if field not in ticket:
                raise StorageError(f"A ticket is missing field: {field}")

        ticket_id = ticket["id"]

        if not isinstance(ticket_id, str):
            raise StorageError("Invalid ticket ID")

        if not re.fullmatch(r"T[0-9]{3,}", ticket_id):
            raise StorageError("Invalid ticket ID")

        if ticket_id in seen_ids:
            raise StorageError("Duplicate ticket ID")

        seen_ids.add(ticket_id)

        try:
            if check_title(ticket["title"]) != ticket["title"]:
                raise ValueError("Invalid title")

            if check_category(ticket["category"]) != ticket["category"]:
                raise ValueError("Invalid category")

            if check_urgency(ticket["urgency"]) != ticket["urgency"]:
                raise ValueError("Invalid urgency")

            check_affected_users(ticket["affected_users"])

        except ValueError as error:
            raise StorageError(f"Invalid ticket data: {error}") from error

        expected_priority = calculate_priority(
            ticket["urgency"],
            ticket["affected_users"]
        )

        if ticket["priority"] != expected_priority:
            raise StorageError("Invalid ticket priority")

        if ticket["status"] not in ("open", "in_progress", "resolved"):
            raise StorageError("Invalid ticket status")

        assigned_to = ticket["assigned_to"]

        if assigned_to is not None:
            if not isinstance(assigned_to, str) or not assigned_to.strip():
                raise StorageError("Invalid assigned staff")

            if assigned_to != assigned_to.strip():
                raise StorageError("Invalid assigned staff")

        if ticket["status"] == "in_progress" and not assigned_to:
            raise StorageError("In-progress ticket must be assigned")

        notes = ticket.get("notes", [])

        if not isinstance(notes, list):
            raise StorageError("Invalid notes format")

        seen_note_ids = set()

        for note in notes:
            if not isinstance(note, dict):
                raise StorageError("Invalid note")

            required_note_fields = {
                "note_id",
                "author",
                "message"
            }

            for field in required_note_fields:
                if field not in note:
                    raise StorageError(f"Missing note field: {field}")

            note_id = note["note_id"]

            if not isinstance(note_id, str):
                raise StorageError("Invalid note ID")

            if not re.fullmatch(r"N[0-9]{3,}", note_id):
                raise StorageError("Invalid note ID")

            if note_id in seen_note_ids:
                raise StorageError("Duplicate note ID")

            seen_note_ids.add(note_id)

            author = note["author"]
            message = note["message"]

            if not isinstance(author, str) or not author.strip():
                raise StorageError("Invalid note author")

            if author != author.strip():
                raise StorageError("Invalid note author")

            if not isinstance(message, str):
                raise StorageError("Invalid note message")

            if not 5 <= len(message) <= 300:
                raise StorageError("Invalid note message")

            if message != message.strip():
                raise StorageError("Invalid note message")

    return tickets


def load_tickets(path=DEFAULT_PATH):
    file_path = Path(path)

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            tickets = json.load(file)

    except json.JSONDecodeError as error:
        raise StorageError(
            f"Ticket file is corrupted: {error}"
        ) from error

    except (OSError, UnicodeError) as error:
        raise StorageError(
            f"Could not read the file: {error}"
        ) from error

    return validate_tickets(tickets)


def save_tickets(tickets, path=DEFAULT_PATH):
    validate_tickets(tickets)

    file_path = Path(path)
    temp_path = file_path.with_name(file_path.name + ".tmp")

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        text = json.dumps(tickets, indent=4)

        with open(temp_path, "w", encoding="utf-8") as file:
            file.write(text)

        temp_path.replace(file_path)

    except (OSError, TypeError, ValueError) as error:
        raise StorageError(
            f"Could not save tickets: {error}"
        ) from error