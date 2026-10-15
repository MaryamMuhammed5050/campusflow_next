from campusflow.workflow import _find_ticket


def add_note(tickets, ticket_id, author, message):
    ticket = _find_ticket(tickets, ticket_id)

    if ticket is None:
        raise ValueError("Ticket not found")

    if ticket["status"] == "resolved":
        raise ValueError("Cannot add notes to resolved tickets")

    if not isinstance(author, str) or not author.strip():
        raise ValueError("Invalid author")

    if not isinstance(message, str) or not 5 <= len(message.strip()) <= 300:
        raise ValueError("Message must contain 5 to 300 characters")

    notes = ticket.get("notes", [])

    highest = max(
        (int(note["note_id"][1:]) for note in notes),
        default=0
    )

    note = {
        "note_id": f"N{highest + 1:03d}",
        "author": author.strip(),
        "message": message.strip()
    }

    if "notes" not in ticket:
        ticket["notes"] = []

    ticket["notes"].append(note)

    return note