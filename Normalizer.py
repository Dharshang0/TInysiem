import re
from datetime import datetime

failed_login_regex = re.compile(
    r'.*Failed password for (invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+)'
)

success_login_regex = re.compile(
    r'.*Accepted password for (\w+) from (\d+\.\d+\.\d+\.\d+)'
)


def normalize(line):
    """Convert raw log line into a normalized event dict."""
    # Failed login
    m = failed_login_regex.match(line)
    if m:
        return {
            "timestamp": datetime.now().timestamp(),
            "event": "failed_login",
            "username": m.group(2),
            "ip": m.group(3)
        }

    # Successful login
    m = success_login_regex.match(line)
    if m:
        return {
            "timestamp": datetime.now().timestamp(),
            "event": "success_login",
            "username": m.group(1),
            "ip": m.group(2)
        }

    return None
