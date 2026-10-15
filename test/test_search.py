import unittest
from copy import deepcopy

from campusflow.search import (
    search_by_title,
    filter_by_category,
    search_tickets,
)


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi outage",
                "category": "Network",
                "status": "open",
                "priority": "critical",
            },
            {
                "id": "T002",
                "title": "Wi-Fi problem",
                "category": "Network",
                "status": "resolved",
                "priority": "critical",
            },
            {
                "id": "T003",
                "title": "Broken laptop",
                "category": "Hardware",
                "status": "open",
                "priority": "critical",
            },
            {
                "id": "T004",
                "title": "Slow internet",
                "category": "Network",
                "status": "open",
                "priority": "low",
            },
        ]

    def test_title_search_is_case_insensitive(self):
        results = search_by_title(self.tickets, "WI-FI")

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001", "T002"],
        )

    def test_category_filter_is_case_insensitive(self):
        results = filter_by_category(
            self.tickets,
            "NETWORK",
        )

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001", "T002", "T004"],
        )

    def test_combined_filters_use_and_logic(self):
        results = search_tickets(
            self.tickets,
            category="Network",
            status="open",
            priority="critical",
        )

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001"],
        )

    def test_single_filter(self):
        results = search_tickets(
            self.tickets,
            status="open",
        )

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001", "T003", "T004"],
        )

    def test_no_filters_returns_all_tickets(self):
        results = search_tickets(self.tickets)

        self.assertEqual(len(results), 4)

    def test_search_does_not_modify_tickets(self):
        original = deepcopy(self.tickets)

        search_tickets(
            self.tickets,
            category="Network",
            status="open",
        )

        self.assertEqual(self.tickets, original)


if __name__ == "__main__":
    unittest.main()