def search_by_title(tickets, search_term):
    results = []

    search_term = search_term.strip().casefold()

    for ticket in tickets:
        title = ticket["title"].casefold()

        if search_term in title:
            results.append(ticket)

    return results


def filter_by_category(tickets, category):
    results = []

    category = category.strip().casefold()

    for ticket in tickets:
        ticket_category = ticket["category"].casefold()

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

    title = title.strip().casefold()
    category = category.strip().casefold()
    status = status.strip().casefold()
    priority = priority.strip().casefold()

    for ticket in tickets:
        if title and title not in ticket["title"].casefold():
            continue

        if category and category != ticket["category"].casefold():
            continue

        if status and status != ticket["status"].casefold():
            continue

        if priority and priority != ticket["priority"].casefold():
            continue

        results.append(ticket)

    return results