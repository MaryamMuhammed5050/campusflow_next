VALID_STATUSES = ["open", "in_progress", "resolved"]
VALID_PRIORITIES = ["critical", "high", "medium", "low"]


def generate_report(tickets):
    """Summarize total count and breakdown by status/priority without altering tickets."""
    if tickets is None:
        tickets = []

    total_tickets = len(tickets)
    status_counts = {status: 0 for status in VALID_STATUSES}
    priority_counts = {priority: 0 for priority in VALID_PRIORITIES}
    
    extra_statuses = {}
    extra_priorities = {}

    for ticket in tickets:
        status = str(ticket.get("status", "open")).lower()
        if status in status_counts:
            status_counts[status] += 1
        else:
            extra_statuses[status] = extra_statuses.get(status, 0) + 1
            
        priority = str(ticket.get("priority", "low")).lower()
        if priority in priority_counts:
            priority_counts[priority] += 1
        else:
            extra_priorities[priority] = extra_priorities.get(priority, 0) + 1

    status_counts.update(extra_statuses)
    priority_counts.update(extra_priorities)

    return {
        "total_tickets": total_tickets,
        "by_status": status_counts,
        "by_priority": priority_counts
    }


def format_report_text(report_data):
    """Format summary output into printable text."""
    lines = [
        "=== CAMPUSFLOW TICKET REPORT ===",
        f"Total Tickets: {report_data['total_tickets']}",
        "",
        "Status Breakdown:"
    ]
    
    for status, count in report_data["by_status"].items():
        lines.append(f"  - {status.replace('_', ' ').title()}: {count}")
        
    lines.append("")
    lines.append("Priority Breakdown:")
    for priority, count in report_data["by_priority"].items():
        lines.append(f"  - {priority.capitalize()}: {count}")
        
    return "\n".join(lines)