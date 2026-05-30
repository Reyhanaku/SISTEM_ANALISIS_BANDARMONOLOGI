import requests
import streamlit as st

GAS_URL = "https://script.google.com/macros/s/AKfycbztzJL_waRDfHgmfgxLZN4em1N6RikwOBAvv7Q-9csLxWCOGAbFPUh219JAmP4Tgw/exec"

@st.cache_data(ttl=300)
def fetch_brokers():
    try:
        res = requests.get(GAS_URL)
        if res.status_code == 200:
            return res.json().get('brokers', [])
    except:
        return []
    return []

def post_data(payload):
    try:
        res = requests.post(GAS_URL, json=payload, allow_redirects=True)
        if res.status_code == 200:
            return res.json()
    except:
        return None
    return None