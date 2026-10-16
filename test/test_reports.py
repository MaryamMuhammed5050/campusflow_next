import unittest
from copy import deepcopy

from campusflow.reports import generate_report, format_report_text

class TestReports(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "category": "Network",
                "status": "open",
                "priority": "critical",
            },
            {
                "id": "T002",
                "category": "Hardware",
                "status": "resolved",
                "priority": "medium",
            },
            {
                "id": "T003",
                "category": "Network",
                "status": "resolved",
                "priority": "high",
            },
            {
                "id": "T004",
                "category": "Software",
                "status": "open",
                "priority": "low",
            },
        ]

    def test_total_tickets(self):
        report = generate_report(self.tickets)

        self.assertEqual(report["total_tickets"], 4)

    def test_status_counts(self):
        report = generate_report(self.tickets)

        self.assertEqual(report["by_status"]["open"], 2)
        self.assertEqual(report["by_status"]["resolved"], 2)
        self.assertEqual(report["by_status"]["in_progress"], 0)

    def test_priority_counts(self):
        report = generate_report(self.tickets)

        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["high"], 1)
        self.assertEqual(report["by_priority"]["medium"], 1)
        self.assertEqual(report["by_priority"]["low"], 1)

    def test_category_counts(self):
        report = generate_report(self.tickets)

        self.assertEqual(report["by_category"]["Network"], 2)
        self.assertEqual(report["by_category"]["Hardware"], 1)
        self.assertEqual(report["by_category"]["Software"], 1)
        self.assertEqual(report["by_category"]["Other"], 0)

    def test_resolved_and_unresolved(self):
        report = generate_report(self.tickets)

        self.assertEqual(report["resolved"], 2)
        self.assertEqual(report["unresolved"], 2)

    def test_resolution_percentage(self):
        report = generate_report(self.tickets)

        self.assertEqual(report["resolution_percentage"], 50.0)

    def test_empty_report(self):
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)

    def test_report_does_not_modify_tickets(self):
        original = deepcopy(self.tickets)

        generate_report(self.tickets)

        self.assertEqual(self.tickets, original)
        
    def test_format_report_text(self):
        report = generate_report(self.tickets)
        text = format_report_text(report)

        self.assertIn("Total Tickets: 4", text)
        self.assertIn("Category Breakdown:", text)
        self.assertIn("Network: 2", text)
        self.assertIn("Resolved Tickets: 2", text)
        self.assertIn("Unresolved Tickets: 2", text)
        self.assertIn("Resolution Percentage: 50.0%", text)


if __name__ == "__main__":
    unittest.main()