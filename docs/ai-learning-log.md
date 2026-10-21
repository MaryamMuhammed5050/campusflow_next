 Project Overview

I used AI as a learning assistant while working on CampusFlow Next. It helped me understand the existing project, break down requirements, and make better decisions when implementing features.

## 2. Areas Where AI Helped

### Understanding the Project
AI helped me understand the project requirements, the existing code structure, and the responsibilities assigned to each engineer.

### Storage and Persistence
AI explained how JSON storage can save ticket information and make it available when the application runs again.

### Reports
AI helped me understand how ticket data can be summarized into useful statistics, such as ticket counts by status, priority, and category.

### Git and GitHub
AI guided me through creating a feature branch, checking Git status, and understanding how changes are committed and submitted for review.

## 3. A Challenge I Faced

I needed to understand how storage and reporting fit into the existing application without breaking its original functionality.

AI helped me break the requirements into smaller tasks and understand the purpose of each component before working on it.

## 4. What I Learned

- Why existing functionality should be checked before making changes.
- How JSON supports data persistence.
- How reports turn ticket records into useful summaries.
- Why automated tests help identify errors.
- Why Git branches and pull requests support team collaboration.

## 5. How I Used AI Responsibly

I used AI to explain concepts, clarify requirements, and guide my work. I understand that I must review, test, and understand any suggested solution before including it in the project.

## 6. Reflection

This project is helping me improve my understanding of Python, software development, and collaborative coding. I still have concepts to practise, but I am learning to ask better questions, understand the solutions, and take greater responsibility for my work.

## 7. Engineer B AI Learning Cycles

### Learning Cycle 1 — Combining Search Filters

**Original concept gap**

I understood how to search for a ticket using one condition, but I was not fully sure how multiple optional filters should work together without accidentally returning unrelated tickets.

**Exact question asked**

"When multiple search filters are supplied, should the filters use AND or OR logic, and how can I make optional filters work without modifying the ticket collection?"

**Summary of AI guidance**

AI explained that the CampusFlow requirements need AND logic. If the user supplies title, category and status, a ticket must satisfy all three conditions. An empty filter should simply be ignored. AI also explained that search should build a new results list instead of changing the original tickets.

**Tiny unrelated experiment**

I tested the idea using a small list of books. Each book had a title and category. I filtered for a word in the title and a specific category. I observed that using separate checks with `continue` kept only books satisfying every supplied condition.

**Independent verification**

I compared the approach with the CampusFlow requirement and ran automated search tests. The tests confirmed that combined filters return only tickets matching all supplied filters and that case-insensitive title searching works.

**Final engineering decision**

I kept `search_tickets()` read-only and used AND-style filtering. Each supplied filter must match before a ticket is appended to the results. Empty filters do not restrict the search.


### Learning Cycle 2 — Work Queue Requirement and Correcting an AI Suggestion

**Original concept gap**

I initially thought the work queue should contain every unresolved ticket, meaning both `open` and `in_progress` tickets.

**Exact question asked**

"Should the CampusFlow work queue contain both open and in-progress tickets, and how should the queue be sorted?"

**Summary of AI guidance**

AI initially suggested treating both `open` and `in_progress` tickets as unresolved work and sorting them by status, priority and ticket ID.

**Tiny unrelated experiment**

I created a small example containing three tasks: one open task, one in-progress task and one completed task. I compared a general unresolved-work queue with a queue whose contract explicitly said "open tasks only." This showed that the correct filter depends on the stated contract rather than the general meaning of unresolved work.

**Independent verification**

Engineer A's review requested that the work queue display only open tickets. I then checked the CampusFlow Next specification, which explicitly states that the original Open Work Queue must contain only OPEN tickets and that `in_progress` and `resolved` tickets must not appear. I updated the tests and ran the full automated test suite.

**What was wrong or missing from the AI suggestion**

The initial AI suggestion used a reasonable general interpretation of "work queue," but it did not follow the project's exact business rule. Including `in_progress` tickets would have changed an original CampusFlow feature that the specification required us to preserve.

**Final engineering decision**

I rejected the original suggestion and restored the queue to filter only tickets whose status is `open`. I sorted those tickets by priority first and numeric ticket ID second. The final full suite passed 122 tests.

**Regression protection**

The workflow tests verify that non-open tickets are excluded and that open tickets are ordered according to the required priority and numeric-ID rules.