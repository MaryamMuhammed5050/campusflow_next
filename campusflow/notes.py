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

    notes = ticket.setdefault("notes", [])

    note = {
        "note_id": f"N{len(notes) + 1:03d}",
        "author": author.strip(),
        "message": message.strip()
    }

    notes.append(note)
    return note