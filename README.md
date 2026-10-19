# Smart IP Address & Subnet Calculator

A Computer Networks mini project written in Python. It takes an IPv4
address with a CIDR prefix (for example `192.168.1.10/24`) and calculates
the subnet mask, wildcard mask, network address, broadcast address,
usable host range, and host counts.

## Features
- Validates IPv4 addresses and CIDR prefixes (0-32) with clear error messages
- Calculates subnet mask, wildcard mask, network and broadcast addresses
- Shows usable host range and counts, with special handling for /31 and /32
- Displays the IP and subnet mask in binary
- Clickable example addresses and a Reset button
- Uses only Python's built-in `ipaddress` module for the calculations

## Technologies
- Python 3.12 (or any Python 3.9+)
- Streamlit (web interface)
- `ipaddress` (built-in calculations)

## How to Run (Windows 11 + VS Code)

```bash
cd smart_ip_calculator
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501 in your browser.

## Note
This tool performs calculations only. It does not scan or discover
any real network devices.
