from campusflow.tickets import create_ticket, find_ticket
from campusflow.workflow import (
    assign_ticket,
    update_status,
    get_work_queue,
)
from campusflow.notes import add_note
from campusflow.search import search_tickets
from campusflow.reports import generate_report, format_report_text
from campusflow.storage import load_tickets, save_tickets, StorageError
from campusflow.understanding_check import run_understanding_check

def show_ticket(ticket):
    print(f"ID: {ticket['id']}")
    print(f"Title: {ticket['title']}")
    print(f"Category: {ticket['category']}")
    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")
    print(f"Assigned to: {ticket.get('assigned_to') or 'Unassigned'}")

    notes = ticket.get("notes", [])

    if notes:
        print("\nNotes:")

        for note in notes:
            print(
                f"{note['note_id']} | "
                f"{note['author']} | "
                f"{note['message']}"
            )


def show_ticket_list(tickets):
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        assignee = ticket.get("assigned_to") or "Unassigned"

        print(
            f"{ticket['id']} | {ticket['title']} | "
            f"{ticket['priority']} | {ticket['status']} | "
            f"{assignee}"
        )


def handle_create(tickets):
    title = input("Title: ")
    category = input("Category (Network/Hardware/Software/Other): ")
    urgency = input("Urgency (low/medium/high): ")
    affected_users = input("Number of affected users: ")

    try:
        affected_users = int(affected_users.strip())

        ticket = create_ticket(
            tickets,
            title,
            category,
            urgency,
            affected_users
        )

        save_tickets(tickets)

    except ValueError as error:
        print(f"Error: {error}")
        return

    except StorageError as error:
        print(f"Ticket created in memory but could not be saved: {error}")
        return

    print(
        f"Created ticket {ticket['id']} "
        f"with priority {ticket['priority']}."
    )


def handle_view_ticket(tickets):
    ticket_id = input("Enter ticket ID: ").strip()

    try:
        ticket = find_ticket(tickets, ticket_id)

    except ValueError as error:
        print(f"Error: {error}")
        return

    show_ticket(ticket)


def handle_assign(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    staff_name = input("Enter staff name: ").strip()

    try:
        ticket = assign_ticket(tickets, ticket_id, staff_name)

        save_tickets(tickets)

    except ValueError as error:
        print(f"Error: {error}")
        return

    except StorageError as error:
        print(f"Assignment changed in memory but could not be saved: {error}")
        return

    print(
        f"Ticket {ticket['id']} assigned to "
        f"{ticket['assigned_to']} successfully."
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


def handle_view_notes(tickets):
    print("\n=== VIEW TICKET NOTES ===")

    ticket_id = input("Enter ticket ID: ").strip()

    try:
        ticket = find_ticket(tickets, ticket_id)
    except ValueError as error:
        print(error)
        return

    notes = ticket.get("notes", [])

    if not notes:
        print("No notes found for this ticket.")
        return

    print(f"\nNotes for {ticket['id']}:")

    for note in notes:
        print(
            f"{note['note_id']} | "
            f"{note['author']} | "
            f"{note['message']}"
        )


def handle_add_note(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    author = input("Enter your name: ")
    message = input("Enter note: ")

    try:
        note = add_note(
            tickets,
            ticket_id,
            author,
            message
        )

        save_tickets(tickets)

    except ValueError as error:
        print(f"Error: {error}")
        return

    except StorageError as error:
        print(f"Note added in memory but could not be saved: {error}")
        return

    print(f"Note {note['note_id']} added successfully.")


def handle_work_queue(tickets):
    queue = get_work_queue(tickets)

    if not queue:
        print("No open tickets in the work queue.")
        return

    print("\n=== WORK QUEUE ===")
    show_ticket_list(queue)


def handle_report(tickets):
    report_data = generate_report(tickets)
    print(format_report_text(report_data))


def choose_option(title, options):
    while True:
        print(f"\n{title}:")
        print("0. Any")

        for number, value in enumerate(options, start=1):
            display_name = value.replace("_", " ").title()
            print(f"{number}. {display_name}")

        choice = input(f"Choose {title.lower()}: ").strip()

        if choice == "0":
            return ""

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(options):
                return options[number - 1]

        print("Invalid choice. Please try again.")


def handle_search(tickets):
    print("\n=== SEARCH TICKETS ===")

    title = input(
        "Title contains (press Enter for any): "
    ).strip()

    category = choose_option(
        "Category",
        ["Network", "Hardware", "Software", "Other"],
    )

    status = choose_option(
        "Status",
        ["open", "in_progress", "resolved"],
    )

    priority = choose_option(
        "Priority",
        ["critical", "high", "medium", "low"],
    )

    results = search_tickets(
        tickets,
        title=title,
        category=category,
        status=status,
        priority=priority,
    )

    if not results:
        print("\nNo matching tickets found.")
        return

    print(f"\nFound {len(results)} matching ticket(s):")
    show_ticket_list(results)

def display_menu():
    print("\n=== CAMPUSFLOW TICKET SYSTEM ===")
    print("1. Create ticket")
    print("2. View all tickets")
    print("3. View a ticket")
    print("4. Assign ticket")
    print("5. Update ticket status")
    print("6. View work queue")
    print("7. Generate report")
    print("8. Add note")
    print("9. Search tickets")
    print("10. Engineering understanding check")
    print("11. View ticket notes")
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

        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

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

        elif choice == "8":
            handle_add_note(tickets)

        elif choice == "9":
            handle_search(tickets)

        elif choice == "10":
            run_understanding_check()
        
        elif choice == "11":
            handle_view_notes(tickets)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option from the menu.")


if __name__ == "__main__":
    main()