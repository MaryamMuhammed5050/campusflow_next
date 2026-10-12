# Design Decisions

Project: CampusFlow (command-line helpdesk ticket manager)
Team: <Fellow A name> and <Fellow B name>

> Items marked **[CONFIRM]** are proposals. Agree on them with your partner and remove the marker once agreed.

---

## 1. Ownership

| Area | Owner | File(s) | Issue |
|---|---|---|---|
| Ticket creation, validation, priority engine | Engineer A | `campusflow/tickets.py`, `tests/test_tickets.py` | #1 |
| Assignment and status workflow | Engineer B | `campusflow/workflow.py`, `tests/test_workflow.py` | #2 |
| Work queue and reports | Engineer B | `campusflow/workflow.py` (queue), `campusflow/reports.py`, `tests/test_workflow.py` | #3 |
| JSON persistence | Shared (**[CONFIRM]** who writes it) | `campusflow/storage.py`, `tests/test_storage.py` | #4 |
| CLI menu | Shared | `main.py` | #5 |
| Documentation | Shared | `README.md`, `docs/` | #6 |

---

## 2. Data structure

- Tickets are stored in memory as a **list of dictionaries**.
- The list is created by `main.py` on startup (from `load_tickets`) and **passed into** each function as the first argument.
- Field names are exactly: `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, `assigned_to`.
- `assigned_to` is `None` when unassigned (saved as `null` in JSON).
- `affected_users` is stored as an integer.

Example:

    {"id": "T001", "title": "Campus Wi-Fi is down", "category": "Network",
     "urgency": "high", "affected_users": 15, "priority": "critical",
     "status": "open", "assigned_to": None}

---

## 3. Allowed values and normalization

- Categories: `Network`, `Hardware`, `Software`, `Other` (stored with this exact capitalisation).
- Urgency: `low`, `medium`, `high` (stored lowercase).
- Status: `open`, `in_progress`, `resolved` (stored lowercase).
- Priority: `critical`, `high`, `medium`, `low`.
- Input is trimmed of surrounding spaces and matched ignoring capital letters, then stored in the official form above.
- Ticket IDs are matched ignoring case and spaces (`" t001 "` finds `T001`).

---

## 4. Priority rules (checked in order, first match wins)

1. high urgency AND 10 or more affected users: `critical`
2. high urgency OR 10 or more affected users: `high`
3. medium urgency OR 3 or more affected users: `medium`
4. everything else: `low`

This is plain Python logic, not an AI model.

---

## 5. Error handling

- Business-logic functions **raise `ValueError`** with a clear message for invalid input, unknown ticket IDs, and invalid transitions.
- Storage functions **raise `StorageError`** (defined in `storage.py`) so the menu can tell a data-file problem from a user input problem.
- Logic files never call `print()` or `input()`. Only `main.py` does.
- Validate first, change second: a rejected action must leave stored tickets unchanged.

---

## 6. Function contracts

| Function | File | Returns | Raises |
|---|---|---|---|
| `create_ticket(tickets, title, category, urgency, affected_users)` | `tickets.py` | the new ticket (also appended to `tickets`) | `ValueError` |
| `find_ticket(tickets, ticket_id)` | `tickets.py` | the matching ticket | `ValueError` if not found |
| `calculate_priority(urgency, affected_users)` | `tickets.py` | priority string | none (inputs already validated) |
| `next_id(existing_tickets)` | `tickets.py` | next ID string | none |
| `assign_ticket(tickets, ticket_id, staff_name)` **[CONFIRM]** | `workflow.py` | updated ticket | `ValueError` |
| `change_status(tickets, ticket_id, new_status)` **[CONFIRM]** | `workflow.py` | updated ticket | `ValueError` |
| `get_work_queue(tickets)` **[CONFIRM]** | `workflow.py` | sorted list of tickets | none |
| `build_report(tickets)` **[CONFIRM]** | `reports.py` | summary (total, by status, by priority) | none |
| `load_tickets(path=DEFAULT_PATH)` | `storage.py` | list of tickets | `StorageError` |
| `save_tickets(tickets, path=DEFAULT_PATH)` | `storage.py` | nothing | `StorageError` |

---

## 7. Workflow rules

- Allowed transitions: `open` to `in_progress`, `in_progress` to `resolved`.
- An unassigned ticket cannot move to `in_progress`.
- A resolved ticket cannot be modified until it is explicitly reopened (status set back to `open`). **[CONFIRM]** whether assigning counts as a modification.
- Skipping steps (for example `open` straight to `resolved`) is rejected. **[CONFIRM]**

---

## 8. Work queue

- The queue is built in `workflow.py`.
- Includes tickets whose status is `open`.  whether `in_progress` tickets also appear (the spec says "open, unresolved").
- Order: `critical`, `high`, `medium`, `low`. Ties are broken by the **numeric** part of the ID, so `T2` comes before `T10`.
- The queue does not change the stored tickets.

---

## 9. Reports

- Show total tickets, count per status, and count per priority.
- Always list every status and priority, including those with a count of zero.
- Zero tickets must not crash the report.
- Reports only read tickets and never change them.

---

## 10. Persistence

- Default file: `data/tickets.json`, listed in `.gitignore`.
- Only `storage.py` touches the file. Only `main.py` triggers loading and saving.
- Missing file: fresh start with an empty list, no error.
- Corrupted or wrongly formatted file: raise `StorageError`. **Do not overwrite the file.**
- An empty (zero-byte) file counts as corrupted. **[CONFIRM]**
- On startup, if loading fails, `main.py` shows the error and **stops**. It never continues with an empty list, because the next save would destroy the data.
- Saving writes to a temporary `.tmp` file, then replaces the real file, so a crash cannot leave a half-written file.
- The data folder is created automatically if missing.
- No separate ID counter is stored. After loading, `next_id` uses the highest existing ID plus one, so IDs stay unique.

---

## 11. Testing approach

- Framework: `unittest`. Run from the project root with `python -m unittest discover -s tests -v`.
- Tests call logic functions directly and never use `input()` or the menu.
- Storage tests use a temporary folder and never touch `data/tickets.json`.
- Each test creates its own data so tests do not depend on each other.

---

## 12. Git workflow
- Every change goes through a PR reviewed and approved by the other fellow.
- Integration fixes also go through a reviewed PR.

---

## 13. Known limitations
- Values are not re-validated when loaded from JSON; only the presence of required fields is checked.
- `next_id` assumes every stored ID looks like `T` followed by digits.
- Menu-level input handling is not covered by automated tests.