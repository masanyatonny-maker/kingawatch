import unittest

from kingawatch.collector import parse_line


class TestCollector(unittest.TestCase):

    def test_failed_login(self):
        line = "Nov 14 08:30:15 server sshd[1234]: Failed password for tonny from 192.168.1.50 port 54321 ssh2"
        event = parse_line(line)

        self.assertEqual(event["event_type"], "failed_login")
        self.assertEqual(event["username"], "tonny")
        self.assertEqual(event["source_ip"], "192.168.1.50")

    def test_successful_login(self):
        line = "Nov 14 08:31:15 server sshd[1234]: Accepted password for tonny from 192.168.1.50 port 54321 ssh2"
        event = parse_line(line)

        self.assertEqual(event["event_type"], "successful_login")

    def test_ignore_unrelated_message(self):
        line = "Nov 14 08:32:15 server sshd[1234]: Connection closed"
        self.assertIsNone(parse_line(line))

    def test_invalid_log(self):
        line = "This is not a valid SSH log"
        self.assertIsNone(parse_line(line))


if __name__ == "__main__":
    unittest.main()
