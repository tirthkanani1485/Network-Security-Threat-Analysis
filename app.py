import streamlit as st
import pandas as pd

# Sample network traffic data
network_data = [
    {"ip": "192.168.1.1", "requests": 10, "url": "safe-site.com"},
    {"ip": "192.168.1.2", "requests": 5000, "url": "normal-site.com"},
    {"ip": "192.168.1.3", "requests": 20, "url": "fake-bank-login.com"},
    {"ip": "192.168.1.4", "requests": 5, "file": "virus.exe"},
]

st.title("🔐 Network Threat Detection System")

# Show raw data
st.subheader("📡 Network Traffic Data")
df = pd.DataFrame(network_data)
st.dataframe(df)

# Detection Functions
def detect_ddos(data):
    alerts = []
    for entry in data:
        if entry.get("requests", 0) > 1000:
            alerts.append(f"DDoS Alert from IP: {entry['ip']} (Requests: {entry['requests']})")
    return alerts

def detect_phishing(data):
    alerts = []
    for entry in data:
        url = entry.get("url", "")
        if "fake" in url or "login" in url:
            alerts.append(f"Phishing Alert: {url}")
    return alerts

def detect_malware(data):
    alerts = []
    for entry in data:
        file = entry.get("file", "")
        if file.endswith(".exe"):
            alerts.append(f"Malware Alert: {file} from IP {entry['ip']}")
    return alerts

# Button to run scan
if st.button("🚀 Run Scan"):
    st.subheader("🔍 Detection Results")

    ddos = detect_ddos(network_data)
    phishing = detect_phishing(network_data)
    malware = detect_malware(network_data)

    if ddos:
        st.error("DDoS Threats Found")
        for d in ddos:
            st.write(d)

    if phishing:
        st.warning("Phishing Threats Found")
        for p in phishing:
            st.write(p)

    if malware:
        st.error("Malware Threats Found")
        for m in malware:
            st.write(m)

    if not (ddos or phishing or malware):
        st.success("No Threats Detected ✅")