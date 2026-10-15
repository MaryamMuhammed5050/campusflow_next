def search_by_title(tickets, search_term):
    results = []

    search_term = search_term.strip().lower()

    for ticket in tickets:
        title = ticket["title"].lower()

        if search_term in title:
            results.append(ticket)

    return results

def filter_by_category(tickets, category):
    results = []

    category = category.strip().lower()

    for ticket in tickets:
        ticket_category = ticket["category"].lower()

        if ticket_category == category:
            results.append(ticket)

    return results

def search_tickets(
    tickets,
    title="",
    category="",
    status="",
    priority=""
):
    results = []

    title = title.strip().lower()
    category = category.strip().lower()
    status = status.strip().lower()
    priority = priority.strip().lower()

    for ticket in tickets:

        if title and title not in ticket["title"].lower():
            continue

        if category and category != ticket["category"].lower():
            continue

        if status and status != ticket["status"].lower():
            continue

        if priority and priority != ticket["priority"].lower():
            continue

        results.append(ticket)

    return results