import json
from rich import print

def send_alert(alert):
    print(f"[bold red]ALERT:[/bold red] {alert['message']}")

    # Append to alerts.jsonl
    with open("alerts.jsonl", "a") as f:
        f.write(json.dumps(alert) + "\n")
