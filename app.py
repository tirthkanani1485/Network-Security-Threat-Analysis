import streamlit as st
import pandas as pd

st.title("🔐 Network Threat Detection System")

# -------------------------------
# Default Data
# -------------------------------
default_data = [
    {"ip": "192.168.1.1", "requests": 10, "url": "safe-site.com", "file": ""},
    {"ip": "192.168.1.2", "requests": 5000, "url": "normal-site.com", "file": ""},
    {"ip": "192.168.1.3", "requests": 20, "url": "fake-bank-login.com", "file": ""},
    {"ip": "192.168.1.4", "requests": 5, "url": "", "file": "virus.exe"},
]

# -------------------------------
# Session State for Data Storage
# -------------------------------
if "data" not in st.session_state:
    st.session_state.data = default_data.copy()

# -------------------------------
# Add Custom Input
# -------------------------------
st.subheader("➕ Add Network Data")

ip = st.text_input("IP Address")
requests = st.number_input("Number of Requests", min_value=0)
url = st.text_input("URL (optional)")
file = st.text_input("File Name (optional)")

if st.button("Add Data"):
    new_entry = {
        "ip": ip,
        "requests": requests,
        "url": url,
        "file": file
    }
    st.session_state.data.append(new_entry)
    st.success("Data Added Successfully ✅")

# -------------------------------
# Show Data
# -------------------------------
st.subheader("📡 Network Traffic Data")
df = pd.DataFrame(st.session_state.data)
st.dataframe(df)

# -------------------------------
# Detection Functions
# -------------------------------
def detect_ddos(data):
    return [f"DDoS Alert from {e['ip']} ({e['requests']} req)"
            for e in data if e.get("requests", 0) > 1000]

def detect_phishing(data):
    return [f"Phishing URL: {e['url']}"
            for e in data if "fake" in e.get("url", "") or "login" in e.get("url", "")]

def detect_malware(data):
    return [f"Malware File: {e['file']} from {e['ip']}"
            for e in data if e.get("file", "").endswith(".exe")]

# -------------------------------
# Run Detection
# -------------------------------
if st.button("🚀 Run Detection"):
    st.subheader("🔍 Results")

    ddos = detect_ddos(st.session_state.data)
    phishing = detect_phishing(st.session_state.data)
    malware = detect_malware(st.session_state.data)

    if ddos:
        st.error("DDoS Threats")
        for d in ddos:
            st.write(d)

    if phishing:
        st.warning("Phishing Threats")
        for p in phishing:
            st.write(p)

    if malware:
        st.error("Malware Threats")
        for m in malware:
            st.write(m)

    if not (ddos or phishing or malware):
        st.success("No Threats Detected ✅")

# -------------------------------
# Reset Button
# -------------------------------
if st.button("🔄 Reset Data"):
    st.session_state.data = default_data.copy()
    st.info("Data Reset to Default")


uploaded_file = st.file_uploader("Upload CSV")

if uploaded_file:
    new_df = pd.read_csv(uploaded_file)
    st.session_state.data.extend(new_df.to_dict("records"))
