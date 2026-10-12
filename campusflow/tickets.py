def check_title(title):
    if not isinstance(title, str):
        raise ValueError("Title must be text")
    
    title = title.strip()
    if len(title) == 0:
        raise ValueError("Title cannot be blank")
        
    return title

def check_category(category):
    if not isinstance(category, str):
        raise ValueError("category must be text")

    cleaned = category.strip().lower()
    allowed_name = ["Network", "Hardware", "Software", "Other"] 

    for official_name in allowed_name:
        if official_name.lower() == cleaned:
            return official_name
        
    raise ValueError("Category must be one of: Network, Hardware, Software, Other")

def check_urgency(urgency):
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be text")

    cleaned = urgency.strip().lower()
    if cleaned != "low" and cleaned != "medium" and cleaned != "high":
        raise ValueError("Urgency must be low, medium or high")

    return cleaned

def check_affected_users(value):
    if isinstance(value, bool):
        raise ValueError("Affected users must be a positive whole number")

    if isinstance(value, int):
        number = value

    elif isinstance(value, str):
        value = value.strip()

        try:
            number = int(value)
        except ValueError:
            raise ValueError("Affected users must be a positive whole number")

    else:
        raise ValueError("Affected users must be a positive whole number")

    if number < 1:
        raise ValueError("Affected users must be a positive whole number")

    return number

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
        ticket_id = ticket["id"]
        number = int(ticket_id[1:])

        if number > highest:
            highest = number

    new_number = highest + 1

    return f"T{new_number:03d}"


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
        "assigned_to": None
    }

    tickets.append(ticket)

    return ticket

def find_ticket(tickets, ticket_id):
    ticket_id = ticket_id.strip().upper()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError("Ticket not found")



    

    

    




