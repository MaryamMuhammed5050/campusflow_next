# CampusFlow Next — Baseline Check

## Engineer
Engineer A — Ticket Safety and Storage

## Repository
https://github.com/MaryamMuhammed5050/campusflow_next

## Purpose
To understand the existing application and verify
its behaviour before introducing new features.

## Baseline Test Command

python3 -m unittest discover -s test -p "test_*.py" -v

## Test Results

Total tests: 50
Passed: 50
Failed: 0
Errors: 0

Result: PASS

## Initial Code Inspection

The existing application supports:

- Ticket creation
- Ticket validation
- Priority calculation
- Ticket assignment
- Status updates
- Work queue
- Reports
- JSON storage

## Potential Problems Requiring Verification

1. Ticket assignment uses inconsistent dictionary keys:
   assigned_to and assignee.

2. The existing work queue includes in_progress
   tickets, although the specification requires
   only open tickets.

3. JSON loading does not yet perform all the
   required business-data validation.

4. Some CLI operations may not handle invalid
   ticket IDs safely.

## Manual Inputs Tested

Pending manual application testing.

## Engineering Decision

Preserve the original application and strengthen
its validation, reliability, and test coverage.

No existing functionality should be removed
without justification.