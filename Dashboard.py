import streamlit as st
import json
import pandas as pd
import time
from datetime import datetime

ALERT_FILE = "alerts.jsonl"
EVENT_FILE = "events.jsonl"

st.set_page_config(page_title="TinySIEM Dashboard", layout="wide")

st.title("🔍 TinySIEM Dashboard")
st.caption("Real-time monitoring and alert visualization")

# --- Load events ---
def load_events():
    events = []
    try:
        with open(EVENT_FILE, "r") as f:
            for line in f:
                events.append(json.loads(line))
    except FileNotFoundError:
        pass
    return events

# --- Load alerts ---
def load_alerts():
    alerts = []
    try:
        with open(ALERT_FILE, "r") as f:
            for line in f:
                alerts.append(json.loads(line))
    except FileNotFoundError:
        pass
    return alerts


# Layout
event_col, alert_col = st.columns(2)

with event_col:
    st.subheader("📁 Incoming Events")
    event_placeholder = st.empty()

with alert_col:
    st.subheader("🚨 Alerts")
    alert_placeholder = st.empty()


# Auto-refresh dashboard
while True:
    events = load_events()
    alerts = load_alerts()

    if events:
        df_events = pd.DataFrame(events)
        event_placeholder.dataframe(df_events.tail(20))

    if alerts:
        df_alerts = pd.DataFrame(alerts)
        alert_placeholder.dataframe(df_alerts.tail(20))

    time.sleep(2)
    st.rerun()
