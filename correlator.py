import json
import time
from collections import defaultdict, deque


class Correlator:
    def __init__(self, rules_path):
        with open(rules_path, "r") as f:
            self.rules = json.load(f)

        # Memory store for events
        self.store = defaultdict(lambda: deque())

    def process_event(self, event):
        """Check all rules against the incoming event."""
        alerts = []

        for rule_name, rule in self.rules.items():
            if "event" in rule:
                alert = self._check_threshold_rule(rule_name, rule, event)
                if alert:
                    alerts.append(alert)

            if "sequence" in rule:
                alert = self._check_sequence_rule(rule_name, rule, event)
                if alert:
                    alerts.append(alert)

        return alerts

    def _check_threshold_rule(self, rule_name, rule, event):
        if event["event"] != rule["event"]:
            return None

        key = event.get(rule["group_by"])
        if key is None:
            return None

        bucket = self.store[(rule_name, key)]
        bucket.append(event["timestamp"])

        now = event["timestamp"]

        while bucket and (now - bucket[0] > rule["window_seconds"]):
            bucket.popleft()

        if len(bucket) >= rule["threshold"]:
            return {
                "rule": rule_name,
                "count": len(bucket),
                "group": key,
                "message": f"{rule_name}: threshold reached for {key}"
            }

        return None

    def _check_sequence_rule(self, rule_name, rule, event):
        key = event.get(rule["group_by"])
        if key is None:
            return None

        bucket = self.store[(rule_name, key)]
        bucket.append((event["event"], event["timestamp"]))

        events_only = [x[0] for x in bucket]

        if events_only[-len(rule["sequence"]):] == rule["sequence"]:
            return {
                "rule": rule_name,
                "group": key,
                "message": f"{rule_name}: sequence detected for {key}"
            }

        return None
