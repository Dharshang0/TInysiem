def collect_logs(path):
    """Yield each log line from a file."""
    with open(path, "r") as f:
        for line in f:
            yield line.strip()
