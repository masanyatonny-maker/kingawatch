import unittest

from kingawatch.detector import detect_brute_force


class TestDetector(unittest.TestCase):

    def test_detect_brute_force(self):
        events = [
            {"event_type": "failed_login", "source_ip": "192.168.1.50"}
            for _ in range(5)
        ]

        alerts = detect_brute_force(events)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["source_ip"], "192.168.1.50")
        self.assertEqual(alerts[0]["failed_attempts"], 5)

    def test_below_threshold(self):
        events = [
            {"event_type": "failed_login", "source_ip": "192.168.1.50"}
            for _ in range(4)
        ]

        alerts = detect_brute_force(events)

        self.assertEqual(alerts, [])

    def test_successful_logins_not_counted(self):
        events = [
            {"event_type": "failed_login", "source_ip": "192.168.1.50"}
            for _ in range(4)
        ]

        events.append({
            "event_type": "successful_login",
            "source_ip": "192.168.1.50"
        })

        alerts = detect_brute_force(events)

        self.assertEqual(alerts, [])

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            detect_brute_force([], threshold=0)


if __name__ == "__main__":
    unittest.main()
