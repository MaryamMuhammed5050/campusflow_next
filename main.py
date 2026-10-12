from campusflow.tickets import create_ticket, find_ticket
from campusflow.workflow import *
from campusflow.reports import *
from campusflow.storage import load_tickets, save_tickets, StorageError
from campusflow.workflow import assign_ticket, update_status
from campusflow.reports import generate_report

def show_ticket(ticket):
    print(f"ID: {ticket['id']}")
    print(f"Title: {ticket['title']}")
    print(f"Category: {ticket['category']}")
    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")

    if ticket["assigned_to"] is None:
        print("Unassigned")
    else:
        print(ticket["assigned_to"])


def show_ticket_list(tickets):
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        assigned_to = ticket["assigned_to"]

        if assigned_to is None:
            assigned_to = "Unassigned"

        print(
            f"{ticket['id']}, {ticket['title']}, "
            f"{ticket['priority']}, {ticket['status']}, "
            f"{assigned_to}"
        )


title = input("Enter ticket title: ")
category = input("Enter ticket category: ")
urgency = input("Enter urgency: ")
affected_users = input("Enter number of affected users: ")

try:
    ticket = create_ticket(title, category, urgency, affected_users)

    tickets = load_tickets()
    tickets.append(ticket)
    save_tickets(tickets)

    print("Ticket created successfully.")

except ValueError as error:
    print(error)

except StorageError as error:
    print(error)
    

def handle_create(tickets):
    title = input("Title: ")
    category = input("Category (Network/Hardware/Software/Other): ")
    urgency = input("Urgency (low/medium/high): ")
    affected_users = input("Number of affected users: ")

    try:
        ticket = create_ticket(
            tickets,
            title,
            category,
            urgency,
            affected_users
        )
    except ValueError as error:
        print(f"Error: {error}")
        return

    try:
        save_tickets(tickets)
    except StorageError as error:
        print(f"Error: {error}")
        return

    print(
        f"Created ticket {ticket['id']} "
        f"with priority {ticket['priority']}"
    )