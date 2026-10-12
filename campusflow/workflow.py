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
    """Assign ticket to staff. Rejects blank names or invalid IDs."""
    if not staff_name or not str(staff_name).strip():
        raise ValueError("Staff name cannot be blank.")
    
    ticket = _find_ticket(tickets, ticket_id)
    if not ticket:
        raise ValueError(f"Ticket ID '{ticket_id}' not found.")
    
    ticket["assignee"] = str(staff_name).strip()
    return ticket


def update_status(tickets, ticket_id, new_status):
    """Update status sequentially (open -> in_progress -> resolved) or reopen."""
    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{new_status}'. Must be one of {VALID_STATUSES}.")
    
    ticket = _find_ticket(tickets, ticket_id)
    if not ticket:
        raise ValueError(f"Ticket ID '{ticket_id}' not found.")
    
    current_status = ticket.get("status", "open")
    
    # Resolved tickets must be reopened first
    if current_status == "resolved":
        if new_status != "open":
            raise ValueError("A resolved ticket cannot be modified unless it is reopened first.")
        ticket["status"] = "open"
        return ticket
    
    # Unassigned tickets cannot start progress
    if new_status == "in_progress":
        assignee = ticket.get("assignee")
        if not assignee or not str(assignee).strip():
            raise ValueError("An unassigned ticket cannot be moved to 'in_progress'.")
    
    # Enforce sequential step transitions
    current_idx = STATUS_ORDER.get(current_status, 0)
    new_idx = STATUS_ORDER.get(new_status, 0)
    
    if new_idx < current_idx:
        raise ValueError(f"Cannot move status backwards from '{current_status}' to '{new_status}'.")
    if new_idx > current_idx + 1:
        raise ValueError(f"Cannot skip steps from '{current_status}' to '{new_status}'.")
    
    ticket["status"] = new_status
    return ticket


def get_work_queue(tickets):
    """Return unresolved tickets (open/in_progress) sorted by priority then ticket ID."""
    unresolved = [
        t for t in tickets 
        if t.get("status") in {"open", "in_progress"}
    ]
    
    def sort_key(t):
        priority = str(t.get("priority", "low")).lower()
        p_weight = PRIORITY_WEIGHTS.get(priority, 4)
        num = _parse_ticket_number(t.get("id", ""))
        return (p_weight, num)
    
    return sorted(unresolved, key=sort_key)