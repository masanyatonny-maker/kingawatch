from collections import Counter


def detect_brute_force(events, threshold=5):
    """Detect possible SSH brute-force attacks."""

    if threshold < 1:
        raise ValueError("Threshold must be at least 1")

    failed_attempts = Counter()

    for event in events:
        if event.get("event_type") == "failed_login":
            source_ip = event.get("source_ip")

            if source_ip:
                failed_attempts[source_ip] += 1

    alerts = []

    for source_ip, count in failed_attempts.items():
        if count >= threshold:
            alerts.append({
                "source_ip": source_ip,
                "failed_attempts": count,
                "alert_type": "possible_brute_force"
            })

    return alerts
