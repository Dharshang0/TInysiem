from collector import collect_logs
from normalizer import normalize
from correlator import Correlator
from alerts import send_alert
import json
import time


def main():
    log_path = "sample_auth.log"   # <-- Replace with /var/log/auth.log if running on Linux
    rules_path = "rules.json"

    print("[*] TinySIEM starting...")
    print(f"[*] Reading from: {log_path}")
    print("[*] Loading rules...")
    
    correlator = Correlator(rules_path)

    # Clear previous session logs (optional)
    open("events.jsonl", "w").close()
    open("alerts.jsonl", "w").close()

    print("[*] Monitoring logs...\n")

    # Main processing loop
    for line in collect_logs(log_path):

        # Normalize raw log line into a structured event
        event = normalize(line)

        if not event:
            continue

        # Write every event to file for the dashboard
        with open("events.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")

        # Process event through correlation engine
        alerts = correlator.process_event(event)

        # If alerts returned, send them
        for alert in alerts:
            send_alert(alert)

        # Sleep to simulate real-time log arrival (optional)
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] TinySIEM stopped by user.")
