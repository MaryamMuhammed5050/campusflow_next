import re

VALID_STATUSES = {"open", "in_progress", "resolved"}
STATUS_ORDER = {"open": 0, "in_progress": 1, "resolved": 2}
PRIORITY_WEIGHTS = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return ticket
    return None


def _parse_ticket_number(ticket_id):
    """Extract numeric value for correct sorting (e.g., T2 before T10)."""
    match = re.search(r'\d+', str(ticket_id))
    return int(match.group()) if match else 0


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign a ticket to a staff member."""

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name must be nonblank text.")


    ticket = _find_ticket(tickets, ticket_id)

    
    if not ticket:
        raise ValueError(f"Ticket ID '{ticket_id}' not found.")

    
    if ticket["status"] == "resolved":
        raise ValueError(
            "Cannot assign a resolved ticket. Reopen it first."
        )

    
    ticket["assigned_to"] = staff_name.strip()

    
    return ticket

def update_status(tickets, ticket_id, new_status):
    if new_status not in VALID_STATUSES:
        raise ValueError("Invalid status")

    ticket = _find_ticket(tickets, ticket_id)
    if ticket is None:
        raise ValueError("Ticket not found")

    current = ticket["status"]

    if current == "resolved":
        if new_status != "open":
            raise ValueError("Reopen resolved ticket first")
    elif new_status != current:
        if STATUS_ORDER[new_status] != STATUS_ORDER[current] + 1:
            raise ValueError("Invalid status transition")

    if new_status == "in_progress":
        if not ticket.get("assigned_to"):
            raise ValueError("Assign ticket first")

    ticket["status"] = new_status
    return ticket

def get_work_queue(tickets):
    open_tickets = [
        ticket for ticket in tickets
        if ticket.get("status") == "open"
    ]

    return sorted(
        open_tickets,
        key=lambda ticket: (
            PRIORITY_WEIGHTS.get(ticket["priority"], 4),
            _parse_ticket_number(ticket["id"])
        )
    )
    # def sort_key(t):
    #     priority = str(t.get("priority", "low")).lower()
    #     p_weight = PRIORITY_WEIGHTS.get(priority, 4)
    #     num = _parse_ticket_number(t.get("id", ""))
    #     return (p_weight, num)
    
    # return sorted(unresolved, key=sort_key)