import json
from pathlib import Path

DEFAULT_PATH = "data/tickets.json"


class StorageError(Exception):
    pass


def load_tickets(path=DEFAULT_PATH):
    file_path = Path(path)

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    except OSError as error:
        raise StorageError(f"Could not read the file: {error}") from error

    try:
        tickets = json.loads(text)
    except json.JSONDecodeError as error:
        raise StorageError(f"Ticket file is corrupted: {error}") from error

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

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise StorageError("Ticket file has the wrong format")

        for field in required_fields:
            if field not in ticket:
                raise StorageError(f"A ticket is missing field: {field}")

    return tickets



def save_tickets(tickets, path=DEFAULT_PATH):
    file_path = Path(path)
    temp_path = file_path.with_name(file_path.name + ".tmp")

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        text = json.dumps(tickets, indent=4)

        with open(temp_path, "w", encoding="utf-8") as file:
            file.write(text)

        temp_path.replace(file_path)

    except (OSError, TypeError, ValueError) as error:
        raise StorageError(f"Could not save tickets: {error}") from error
