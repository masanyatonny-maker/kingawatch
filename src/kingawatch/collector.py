
import re


LOG_PATTERN = re.compile(
    r"(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}) "
    r"(?P<host>\S+) sshd(?:\[\d+\])?: "
    r"(?P<message>.*)"
)

FAILED_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?(?P<username>\S+) "
    r"from (?P<source_ip>\S+)"
)

SUCCESS_PATTERN = re.compile(
    r"Accepted password for (?P<username>\S+) "
    r"from (?P<source_ip>\S+)"
)


def parse_line(line):
    """Convert one SSH log line into a structured event."""

    log_match = LOG_PATTERN.search(line)

    if not log_match:
        return None

    message = log_match.group("message")

    failed_match = FAILED_PATTERN.search(message)
    success_match = SUCCESS_PATTERN.search(message)

    if failed_match:
        match = failed_match
        event_type = "failed_login"
    elif success_match:
        match = success_match
        event_type = "successful_login"
    else:
        return None

    return {
        "timestamp": log_match.group("timestamp"),
        "host": log_match.group("host"),
        "event_type": event_type,
        "username": match.group("username"),
        "source_ip": match.group("source_ip"),
        "raw": line.strip(),
    }


def collect_events(file_path):
    """Read a log file and return recognized authentication events."""

    events = []

    with open(file_path, "r", encoding="utf-8") as log_file:
        for line in log_file:
            event = parse_line(line)

            if event is not None:
                events.append(event)

    return events





