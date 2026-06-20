# ==============================
# FILE: dashboard (4).py 
# ==============================

import streamlit as st
from zoneinfo import ZoneInfo
import sys

st.write(sys.version)

from datetime import datetime

from monday_api import get_monday_items
from reporting import (
    build_tommy_elite_report,
    build_universal_report,
    build_mccormick_report,
    build_nova_report,
    build_appointment_counts
)

st.set_page_config(
    page_title="Confirmation",
    layout="wide"
)

# --- CHANGE HERE: Fetch data when needed (and rely on the caching in monday_api.py) ---
items = get_monday_items() 

page = st.sidebar.selectbox(
    "Select Page",
    [
        "Confirmation",
        "Appointment Counts"
    ]
)

if page == "Confirmation":

    st.title("Confirmation")

    # We use the 'items' variable fetched above
    with st.container(): # Use a container for better layout structure
        tab1, tab2, tab3, tab4 = st.tabs([
            "Tommy & Elite EOD",
            "Universal EOD",
            "McCormick EOD",
            "Nova EOD"
        ])

        # Only run the reports if items were successfully retrieved
        if items: 
            with tab1:
                report = build_tommy_elite_report(items)
                c1,c2,c3,c4 = st.columns(4)
                c1.metric("Confirmed", report["confirmed"])
                c2.metric("Same Day", report["same_day"])
                c3.metric("Same Day %", f'{report["same_day_percent"]}%')
                c4.metric("Conversion %", f'{report["conversion"]}%')

                st.divider()

                c1,c2 = st.columns(2)
                c1.metric("Tommy", report["tommy"])
                c2.metric("Elite", report["elite"])

                st.divider()

                c1,c2,c3,c4 = st.columns(4)
                c1.metric("No Answer", report["no_answer"])
                c2.metric("Cancelled", report["cancelled"])
                c3.metric("Reschedule", report["reschedule"])
                c4.metric("Rejected", report["rejected"])

            with tab2:
                report = build_universal_report(items)
            
                c1, c2 = st.columns(2)
                c1.metric("Confirmed", report["confirmed"])
                c2.metric("Conversion %", f'{report["conversion"]}%')
            
                st.divider()
            
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("No Answer", report["no_answer"])
                c2.metric("Cancelled", report["cancelled"])
                c3.metric("Reschedule", report["reschedule"])
                c4.metric("Rejected", report["rejected"])

            with tab3:
                report = build_mccormick_report(items)
            
                c1, c2 = st.columns(2)
                c1.metric("Confirmed", report["confirmed"])
                c2.metric("Conversion %", f'{report["conversion"]}%')
            
                st.divider()
            
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("No Answer", report["no_answer"])
                c2.metric("Cancelled", report["cancelled"])
                c3.metric("Reschedule", report["reschedule"])
                c4.metric("Rejected", report["rejected"])

            with tab4:
                report = build_nova_report(items)
            
                c1, c2 = st.columns(2)
                c1.metric("Confirmed", report["confirmed"])
                c2.metric("Conversion %", f'{report["conversion"]}%')
            
                st.divider()
            
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("No Answer", report["no_answer"])
                c2.metric("Cancelled", report["cancelled"])
                c3.metric("Reschedule", report["reschedule"])
                c4.metric("Rejected", report["rejected"])
                
        else:
            # Display a message if no data is available for reporting
            col1, col2 = st.columns(2)
            col1.info("Data Unavailable")
            col2.warning("Please check your API keys or board settings.")


# Note: The remaining "Appointment Counts" logic would go here 
# and should also be wrapped with data checking if implemented later.
if page == "Appointment Counts":

    st.title("Appointment Counts")

    counts = build_appointment_counts(items)

    st.write(counts)
    
        
            
