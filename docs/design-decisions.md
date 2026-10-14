CampusFlow Next — Design Decisions

1. Extend the Existing Project: Build on the original CampusFlow instead of rewriting it. Preserve existing features and follow the current project structure.

2. Establish a Baseline: Run the existing application and tests before making changes. Document the results in `docs/baseline-check.md`.

3. Keep the Design Simple:Use Python's standard library and maintain clear separation between validation, workflow, storage, search, reports, and CLI responsibilities. Avoid unnecessary frameworks or new technologies.

4. Protect Data Integrity: Validate inputs before changing ticket data. Invalid operations must not modify existing records.

5. Preserve JSON Persistence:Continue using JSON to save and load tickets and notes. Handle invalid data safely and maintain unique IDs.

6. Agree on Shared Interfaces: Engineer A and Engineer B must agree on ticket fields, function signatures, and error handling before implementing connected features.

7. Test and Review Changes: Add tests for new features, use separate Git branches, and review each other's pull requests before merging into `main`.