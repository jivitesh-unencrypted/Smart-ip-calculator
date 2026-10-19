"""
Smart IP Address and Subnet Calculator
Computer Networks Academic Project
Built with Python's ipaddress module and Streamlit.
"""

import ipaddress
import streamlit as st

# ---------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Smart IP & Subnet Calculator",
    page_icon="🌐",
    layout="wide",
)

# ---------------------------------------------------------------
# CUSTOM STYLING (cards, responsive layout, clean look)
# ---------------------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f4e79;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #555;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }
    .card {
        background: #f4f8fc;
        border-left: 5px solid #1f77b4;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .card-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .card-value {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0b2540;
        font-family: "Consolas", "Courier New", monospace;
        word-break: break-all;
    }
        .range-box {
        background: #eef7ee;
        color: #000000;
        border: 1px solid #b7dcb7;
        border-radius: 8px;
        padding: 16px;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 1rem;
        line-height: 1.9;
    }
    .footer {
        text-align: center;
        color: #777;
        font-size: 0.9rem;
        margin-top: 40px;
        padding-top: 14px;
        border-top: 1px solid #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# SESSION STATE (used for example buttons and the Reset button)
# ---------------------------------------------------------------
if "ip_input" not in st.session_state:
    st.session_state.ip_input = "192.168.1.10"
if "cidr_input" not in st.session_state:
    st.session_state.cidr_input = 24


def set_example(ip, cidr):
    """Fill the input boxes with an example address."""
    st.session_state.ip_input = ip
    st.session_state.cidr_input = cidr


def reset_form():
    """Clear the inputs back to defaults."""
    st.session_state.ip_input = ""
    st.session_state.cidr_input = 24


# ---------------------------------------------------------------
# CALCULATION LOGIC
# ---------------------------------------------------------------
def get_ip_class(first_octet):
    """Return the classful address class (A-E) based on the first octet."""
    if first_octet < 128:
        return "A"
    elif first_octet < 192:
        return "B"
    elif first_octet < 224:
        return "C"
    elif first_octet < 240:
        return "D (Multicast)"
    else:
        return "E (Reserved)"


def calculate_subnet(ip_text, cidr):
    """
    Validate the input and calculate all subnet details.
    Returns (result_dict, error_message). One of the two is None.
    """
    # 1. Validate the IPv4 address
    ip_text = ip_text.strip()
    if not ip_text:
        return None, "Please enter an IPv4 address (example: 192.168.1.10)."

    try:
        ip_obj = ipaddress.IPv4Address(ip_text)
    except ValueError:
        return None, (
            f"'{ip_text}' is not a valid IPv4 address. "
            "An IPv4 address has four numbers (0-255) separated by dots, "
            "like 192.168.1.10."
        )

    # 2. Validate the CIDR prefix
    if cidr is None or not (0 <= int(cidr) <= 32):
        return None, "The CIDR prefix must be a whole number between 0 and 32."

    cidr = int(cidr)

    # 3. Build the network (strict=False lets host bits be set, e.g. 192.168.1.10/24)
    network = ipaddress.IPv4Network(f"{ip_text}/{cidr}", strict=False)

    # 4. Basic values
    total_addresses = network.num_addresses
    network_address = network.network_address
    broadcast_address = network.broadcast_address
    subnet_mask = network.netmask
    wildcard_mask = network.hostmask

    # 5. Usable host range and count (special cases for /31 and /32)
    if cidr == 32:
        usable_count = 1
        first_host = ip_obj
        last_host = ip_obj
        host_note = (
            "/32 is a single-host route. The only address is the host itself, "
            "so there is no separate network or broadcast address."
        )
        network_address = ip_obj
        broadcast_address = ip_obj
    elif cidr == 31:
        usable_count = 2
        first_host = network.network_address
        last_host = network.broadcast_address
        host_note = (
            "/31 is a point-to-point link (RFC 3021). Both addresses are "
            "usable hosts, so the usual network and broadcast addresses "
            "are not reserved."
        )
    else:
        usable_count = total_addresses - 2
        first_host = network.network_address + 1
        last_host = network.broadcast_address - 1
        host_note = (
            "Standard subnet: the first address is the network address and the "
            "last is the broadcast address. Both are reserved and cannot be "
            "assigned to a device."
        )

    # 6. Build the result dictionary
    result = {
        "ip": str(ip_obj),
        "cidr": cidr,
        "ip_class": get_ip_class(int(str(ip_obj).split(".")[0])),
        "is_private": ip_obj.is_private,
        "subnet_mask": str(subnet_mask),
        "wildcard_mask": str(wildcard_mask),
        "network_address": str(network_address),
        "broadcast_address": str(broadcast_address),
        "first_host": str(first_host),
        "last_host": str(last_host),
        "total_addresses": total_addresses,
        "usable_hosts": usable_count,
        "binary_ip": ".".join(f"{int(octet):08b}" for octet in ip_text.split(".")),
        "binary_mask": ".".join(f"{int(octet):08b}" for octet in str(subnet_mask).split(".")),
        "host_note": host_note,
    }
    return result, None


# ---------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------
st.markdown('<div class="main-title">🌐 Smart IP Address & Subnet Calculator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Enter an IPv4 address and its CIDR prefix to find the network, '
    'broadcast, and usable host details.</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------------
col_input, col_examples = st.columns([2, 1])

with col_input:
    st.subheader("Enter Details")
    ip_value = st.text_input(
        "IPv4 Address",
        key="ip_input",
        placeholder="e.g. 192.168.1.10",
    )
    cidr_value = st.number_input(
        "CIDR Prefix (0 to 32)",
        min_value=0,
        max_value=32,
        step=1,
        key="cidr_input",
    )

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        calculate_clicked = st.button("Calculate", type="primary", use_container_width=True)
    with btn_col2:
        st.button("Reset", on_click=reset_form, use_container_width=True)

with col_examples:
    st.subheader("Try an Example")
    st.caption("Click any example to fill the form, then press Calculate.")
    examples = [
        ("192.168.1.10", 24),
        ("10.0.0.25", 16),
        ("172.16.5.20", 20),
        ("192.168.1.1", 31),
        ("10.10.10.10", 32),
    ]
    for ip, cidr in examples:
        st.button(
            f"{ip}/{cidr}",
            key=f"ex_{ip}_{cidr}",
            on_click=set_example,
            args=(ip, cidr),
            use_container_width=True,
        )

# ---------------------------------------------------------------
# RESULTS SECTION
# ---------------------------------------------------------------
if calculate_clicked:
    result, error = calculate_subnet(ip_value, cidr_value)

    if error:
        st.error(f"⚠️ Input Error: {error}")
    else:
        st.success(f"Results for {result['ip']}/{result['cidr']}")

        if result["cidr"] in (31, 32):
            st.info(f"ℹ️ {result['host_note']}")

        # Row 1: key facts as cards
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="card"><div class="card-label">IP Class</div>'
                f'<div class="card-value">{result["ip_class"]}</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="card"><div class="card-label">Subnet Mask</div>'
                f'<div class="card-value">{result["subnet_mask"]}</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="card"><div class="card-label">Wildcard Mask</div>'
                f'<div class="card-value">{result["wildcard_mask"]}</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="card"><div class="card-label">Prefix Length</div>'
                f'<div class="card-value">/{result["cidr"]}</div></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="card"><div class="card-label">Network Address</div>'
                f'<div class="card-value">{result["network_address"]}</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="card"><div class="card-label">Broadcast Address</div>'
                f'<div class="card-value">{result["broadcast_address"]}</div></div>',
                unsafe_allow_html=True,
            )

        # Row 2: visual host range
        st.subheader("Network Visual")
        st.markdown(
            f"""
            <div class="range-box">
            <b>Network Address :</b> {result['network_address']}<br>
            <b>Usable Host Range :</b> {result['first_host']} &nbsp;→&nbsp; {result['last_host']}<br>
            <b>Broadcast Address :</b> {result['broadcast_address']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Row 3: subnet details table
        st.subheader("Subnet Details")
        st.table(
            {
                "Property": [
                    "IP Address",
                    "Is Private IP?",
                    "Total Addresses",
                    "Usable Host Addresses",
                    "First Usable Host",
                    "Last Usable Host",
                ],
                "Value": [
                    result["ip"],
                    "Yes" if result["is_private"] else "No (Public)",
                    f"{result['total_addresses']:,}",
                    f"{result['usable_hosts']:,}",
                    result["first_host"],
                    result["last_host"],
                ],
            }
        )

        # Row 4: binary representation
        st.subheader("Binary Representation")
        st.code(
            f"IP Address : {result['binary_ip']}\n"
            f"Subnet Mask: {result['binary_mask']}",
            language="text",
        )

# ---------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------
st.markdown(
    '<div class="footer">Computer Networks Academic Project · '
    'B.Tech CSE · Built with Python and Streamlit</div>',
    unsafe_allow_html=True,
)
