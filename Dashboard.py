import streamlit as st
import json
import os
import time

st.set_page_config(
    page_title="TinySIEM Dashboard",
    layout="wide",
    page_icon="🔍"
)

# Auto-refresh every 5 seconds
st.title("🔍 TinySIEM Dashboard")
st.caption("Real-time monitoring and alert visualization")

st.markdown("""---""")

# --------------------- Helper Functions ---------------------
def load_log(path):
    """Safely load JSON lines log file."""
    if not os.path.exists(path):
        return []

    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data.append(json.loads(line))
                except:
                    pass
    return data

# --------------------- Layout ---------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Incoming Events")

    events = load_log("events.log")

    if len(events) == 0:
        st.info("No events received yet. Waiting for incoming logs...")
    else:
        st.json(events[-20:])  # Show last 20 events


with col2:
    st.subheader("🚨 Alerts")

    alerts = load_log("alerts.log")

    if len(alerts) == 0:
        st.success("No alerts triggered. System is stable.")
    else:
        st.json(alerts[-20:])  # Show last 20 alerts

# --------------------- Refresh Notice ---------------------
st.markdown("---")
st.caption("Auto-refreshing every 5 seconds…")
time.sleep(5)
st.experimental_set_query_params(refresh=str(time.time()))
