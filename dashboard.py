# ==============================
# FILE: dashboard (4).py 
# ==============================

import streamlit as st
from zoneinfo import ZoneInfo
import sys

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

    st.header("Rep Capacity")

    oregon_reps = st.number_input(
        "Oregon Reps",
        min_value=0,
        value=4
    )

    washington_reps = st.number_input(
        "Washington Reps",
        min_value=0,
        value=3
    )

    socal_reps = st.number_input(
        "Southern California Reps",
        min_value=0,
        value=5
    )

    st.subheader("Capacity")
    
    total_capacity = (
        (oregon_reps * 3)
        + (washington_reps * 3)
        + (socal_reps * 3)
    )
    
    st.write(
        f"OR: {oregon_reps * 3}    "
        f"WA: {washington_reps * 3}    "
        f"CA: {socal_reps * 3}    "
        f"TOTAL: {total_capacity}"
    )

    today_or = (
        counts["oregon"]["today"]["10-12"]
        + counts["oregon"]["today"]["1-3"]
        + counts["oregon"]["today"]["4-6"]
    )
    
    today_wa = (
        counts["washington"]["today"]["10-12"]
        + counts["washington"]["today"]["1-3"]
        + counts["washington"]["today"]["4-6"]
    )
    
    today_ca = (
        counts["socal"]["today"]["10-12"]
        + counts["socal"]["today"]["1-3"]
        + counts["socal"]["today"]["4-6"]
    )
    
    today_total = (
        today_or
        + today_wa
        + today_ca
    )
    
    st.subheader("Today")
    
    st.write(
        f"OR: {today_or}    "
        f"WA: {today_wa}    "
        f"CA: {today_ca}    "
        f"TOTAL: {today_total}    "
        f"ATM: {total_capacity}"
    )

    tomorrow_or = (
        counts["oregon"]["tomorrow"]["10-12"]
        + counts["oregon"]["tomorrow"]["1-3"]
        + counts["oregon"]["tomorrow"]["4-6"]
    )
    
    tomorrow_wa = (
        counts["washington"]["tomorrow"]["10-12"]
        + counts["washington"]["tomorrow"]["1-3"]
        + counts["washington"]["tomorrow"]["4-6"]
    )
    
    tomorrow_ca = (
        counts["socal"]["tomorrow"]["10-12"]
        + counts["socal"]["tomorrow"]["1-3"]
        + counts["socal"]["tomorrow"]["4-6"]
    )
    
    tomorrow_total = (
        tomorrow_or
        + tomorrow_wa
        + tomorrow_ca
    )
    
    st.subheader("Tomorrow")
    
    st.write(
        f"OR: {tomorrow_or}    "
        f"WA: {tomorrow_wa}    "
        f"CA: {tomorrow_ca}    "
        f"TOTAL: {tomorrow_total}    "
        f"ATM: {total_capacity}"
    )

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Today")

    with right_col:
        st.subheader("Tomorrow")

    oregon_booked = (
        counts["oregon"]["tomorrow"]["10-12"]
        + counts["oregon"]["tomorrow"]["1-3"]
        + counts["oregon"]["tomorrow"]["4-6"]
    )
    
    washington_booked = (
        counts["washington"]["tomorrow"]["10-12"]
        + counts["washington"]["tomorrow"]["1-3"]
        + counts["washington"]["tomorrow"]["4-6"]
    )
    
    socal_booked = (
        counts["socal"]["tomorrow"]["10-12"]
        + counts["socal"]["tomorrow"]["1-3"]
        + counts["socal"]["tomorrow"]["4-6"]
    )
    
    st.write(
        f"OR: {oregon_booked} appointments"
    )
    
    st.write(
        f"WA: {washington_booked} appointments"
    )
    
    st.write(
        f"CA: {socal_booked} appointments"
    )
    
    st.subheader("Status")
    
    oregon_capacity = oregon_reps * 3
    washington_capacity = washington_reps * 3
    socal_capacity = socal_reps * 3
    
    st.write(
        "Oregon:",
        f"{oregon_booked}/{oregon_capacity}"
    )
    
    st.write(
        "Washington:",
        f"{washington_booked}/{washington_capacity}"
    )
    
    st.write(
        "SoCal:",
        f"{socal_booked}/{socal_capacity}"
    )
            
