
from campusflow.tickets import create_ticket, find_ticket
from campusflow.workflow import (
    assign_ticket,
    update_status,
    get_work_queue,
)
from campusflow.reports import generate_report, format_report_text
from campusflow.storage import load_tickets, save_tickets, StorageError


def show_ticket(ticket):
    print(f"ID: {ticket['id']}")
    print(f"Title: {ticket['title']}")
    print(f"Category: {ticket['category']}")
    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")

    assignee = ticket.get("assignee") or ticket.get("assigned_to")

    if not assignee:
        print("Assigned to: Unassigned")
    else:
        print(f"Assigned to: {assignee}")


def show_ticket_list(tickets):
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        assignee = ticket.get("assignee") or ticket.get("assigned_to")
        assignee = assignee or "Unassigned"

        print(
            f"{ticket['id']} | {ticket['title']} | "
            f"{ticket['priority']} | {ticket['status']} | "
            f"{assignee}"
        )


def handle_create(tickets):
    title = input("Title: ")
    category = input(
        "Category (Network/Hardware/Software/Other): "
    )
    urgency = input("Urgency (low/medium/high): ")
    affected_users = input("Number of affected users: ")

    try:
        ticket = create_ticket(
            tickets,
            title,
            category,
            urgency,
            affected_users,
        )
    except ValueError as error:
        print(f"Error: {error}")
        return

    try:
        save_tickets(tickets)
    except StorageError as error:
        print(f"Ticket created in memory but could not be saved: {error}")
        return

    print(
        f"Created ticket {ticket['id']} "
        f"with priority {ticket['priority']}."
    )


def handle_view_ticket(tickets):
    ticket_id = input("Enter ticket ID: ").strip()

    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        print(f"Ticket ID '{ticket_id}' not found.")
        return

    show_ticket(ticket)


def handle_assign(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    staff_name = input("Enter staff name: ").strip()

    try:
        ticket = assign_ticket(tickets, ticket_id, staff_name)

        # Keep the storage/display field consistent with older tickets.
        ticket["assigned_to"] = ticket["assignee"]

        save_tickets(tickets)
    except ValueError as error:
        print(f"Error: {error}")
        return
    except StorageError as error:
        print(f"Assignment changed in memory but could not be saved: {error}")
        return

    print(
        f"Ticket {ticket['id']} assigned to "
        f"{ticket['assignee']} successfully."
    )


def handle_update_status(tickets):
    ticket_id = input("Enter ticket ID: ").strip()

    print("Available statuses: open, in_progress, resolved")
    new_status = input("Enter new status: ").strip().lower()

    try:
        ticket = update_status(tickets, ticket_id, new_status)
        save_tickets(tickets)
    except ValueError as error:
        print(f"Error: {error}")
        return
    except StorageError as error:
        print(f"Status changed in memory but could not be saved: {error}")
        return

    print(
        f"Ticket {ticket['id']} status updated to "
        f"{ticket['status']}."
    )


def handle_work_queue(tickets):
    queue = get_work_queue(tickets)

    if not queue:
        print("No unresolved tickets in the work queue.")
        return

    print("\n=== WORK QUEUE ===")
    show_ticket_list(queue)


def handle_report(tickets):
    report_data = generate_report(tickets)
    print(format_report_text(report_data))


def display_menu():
    print("\n=== CAMPUSFLOW TICKET SYSTEM ===")
    print("1. Create ticket")
    print("2. View all tickets")
    print("3. View a ticket")
    print("4. Assign ticket")
    print("5. Update ticket status")
    print("6. View work queue")
    print("7. Generate report")
    print("0. Exit")


def main():
    try:
        tickets = load_tickets()
    except StorageError as error:
        print(f"Could not load tickets: {error}")
        return

    print(f"Loaded {len(tickets)} ticket(s).")

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_create(tickets)

        elif choice == "2":
            show_ticket_list(tickets)

        elif choice == "3":
            handle_view_ticket(tickets)

        elif choice == "4":
            handle_assign(tickets)

        elif choice == "5":
            handle_update_status(tickets)

        elif choice == "6":
            handle_work_queue(tickets)

        elif choice == "7":
            handle_report(tickets)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option from the menu.")


if __name__ == "__main__":
    main()
