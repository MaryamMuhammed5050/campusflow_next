def check_title(title):
    if not isinstance(title, str):
        raise ValueError("Title must be text")

    title = title.strip()

    if not title:
        raise ValueError("Title cannot be blank")

    return title


def check_category(category):
    if not isinstance(category, str):
        raise ValueError("category must be text")

    cleaned = category.strip().lower()
    allowed_names = ["Network", "Hardware", "Software", "Other"]

    for name in allowed_names:
        if name.lower() == cleaned:
            return name

    raise ValueError("Category must be one of: Network, Hardware, Software, Other")


def check_urgency(urgency):
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be text")

    cleaned = urgency.strip().lower()

    if cleaned not in ["low", "medium", "high"]:
        raise ValueError("Urgency must be low, medium or high")

    return cleaned


def check_affected_users(value):
    if type(value) is not int or value < 1:
        raise ValueError("Affected users must be a positive whole number")

    return value


def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def next_id(existing_tickets):
    highest = 0

    for ticket in existing_tickets:
        number = int(ticket["id"][1:])

        if number > highest:
            highest = number

    return f"T{highest + 1:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    clean_title = check_title(title)
    clean_category = check_category(category)
    clean_urgency = check_urgency(urgency)
    clean_users = check_affected_users(affected_users)

    priority = calculate_priority(clean_urgency, clean_users)
    new_id = next_id(tickets)

    ticket = {
        "id": new_id,
        "title": clean_title,
        "category": clean_category,
        "urgency": clean_urgency,
        "affected_users": clean_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
        "notes": []
    }

    tickets.append(ticket)

    return ticket


def find_ticket(tickets, ticket_id):
    if not isinstance(ticket_id, str):
        raise ValueError("Ticket ID must be text")

    ticket_id = ticket_id.strip().upper()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError("Ticket not found")