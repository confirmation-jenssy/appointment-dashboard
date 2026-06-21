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
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        oregon_reps = st.number_input(
            "OR Reps",
            min_value=0,
            value=2
        )
    
    with c2:
        washington_reps = st.number_input(
            "WA Reps",
            min_value=0,
            value=2
        )

    with c3:
        socal_reps = st.number_input(
            "CA Reps",
            min_value=0,
            value=2
        )

    st.subheader("Performance")

    confirmation_rate = st.number_input(
        "Confirmation Rate %",
        min_value=1,
        max_value=100,
        value=50
    )

    lead_multiplier = 100 / confirmation_rate

    # CAPACITY
    
    oregon_target = round(
        (oregon_reps * 3)
        * lead_multiplier
    )
    
    washington_target = round(
        (washington_reps * 3)
        * lead_multiplier
    )
    
    socal_target = round(
        (socal_reps * 3)
        * lead_multiplier
    )
    
    st.subheader("Capacity")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "OR",
        oregon_target,
        f"{oregon_reps} reps"
    )
    
    c2.metric(
        "WA",
        washington_target,
        f"{washington_reps} reps"
    )
    
    c3.metric(
        "CA",
        socal_target,
        f"{socal_reps} reps"
    )

    # TODAY
    
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
    
    # TOMORROW
    
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
    
    # SIDE BY SIDE
    
    left_col, right_col = st.columns(2)
    
    with left_col:

        st.subheader("Today")
    
        c1, c2, c3, c4 = st.columns(4)
    
        c1.metric("OR", today_or)
        c2.metric("WA", today_wa)
        c3.metric("CA", today_ca)
        c4.metric("TOTAL", today_total)
    
    with right_col:

        st.subheader("Tomorrow")
    
        c1, c2, c3, c4 = st.columns(4)
    
        c1.metric("OR", tomorrow_or)
        c2.metric("WA", tomorrow_wa)
        c3.metric("CA", tomorrow_ca)
        c4.metric("TOTAL", tomorrow_total)

    st.divider()

    left_col, right_col = st.columns(2)

    def get_status(booked, capacity):

        if booked < (capacity * 0.75):
            return "🟡 NEED LEADS"
    
        elif booked <= capacity:
            return "🟢 FULL"
    
        return "🔴 OVERBOOKED"
    
    with left_col:

        st.subheader("Today")
        
        or_today = (
            counts["oregon"]["today"]["10-12"]
            + counts["oregon"]["today"]["1-3"]
            + counts["oregon"]["today"]["4-6"]
        )
        
        wa_today = (
            counts["washington"]["today"]["10-12"]
            + counts["washington"]["today"]["1-3"]
            + counts["washington"]["today"]["4-6"]
        )
        
        ca_today = (
            counts["socal"]["today"]["10-12"]
            + counts["socal"]["today"]["1-3"]
            + counts["socal"]["today"]["4-6"]
        )
        
        st.markdown(get_status(or_today, oregon_target)
        )
        
        slot_target = round(
            oregon_target / 3
        )
        
        slot_booked = counts["oregon"]["today"]["10-12"]
        
        st.write(
            f"10AM-12PM: {slot_booked}/{slot_target} "
            f"{get_slot_status(slot_booked, slot_target)}"
        )
        
        slot_target = round(
            oregon_target / 3
        )
        
        slot_booked = counts["oregon"]["today"]["1-3"]
        
        st.write(
            f"1PM-3PM: {slot_booked}/{slot_target} "
            f"{get_slot_status(slot_booked, slot_target)}"
        )
        
        slot_target = round(
            oregon_target / 3
        )
        
        slot_booked = counts["oregon"]["today"]["4-6"]
        
        st.write(
            f"4PM-6PM: {slot_booked}/{slot_target} "
            f"{get_slot_status(slot_booked, slot_target)}"
        )
        
        st.markdown(
            f"**WA {get_status(wa_today, washington_target)}**"
        )
        
        st.write(
            f"10-12: {counts['washington']['today']['10-12']}"
        )
        
        st.write(
            f"1-3: {counts['washington']['today']['1-3']}"
        )
        
        st.write(
            f"4-6: {counts['washington']['today']['4-6']}"
        )
        
        st.markdown(
            f"**CA {get_status(ca_today, socal_target)}**"
        )
        
        st.write(
            f"10-12: {counts['socal']['today']['10-12']}"
        )
        
        st.write(
            f"1-3: {counts['socal']['today']['1-3']}"
        )
        
        st.write(
            f"4-6: {counts['socal']['today']['4-6']}"
        )
    
    with right_col:
        
        st.subheader("Tomorrow")
        
        st.markdown(
            f"**OR {get_status(tomorrow_or, oregon_target)}**"
        )
        
        st.write(
            f"10-12: {counts['oregon']['tomorrow']['10-12']}"
        )
        
        st.write(
            f"1-3: {counts['oregon']['tomorrow']['1-3']}"
        )
        
        st.write(
            f"4-6: {counts['oregon']['tomorrow']['4-6']}"
        )
        
        st.markdown(
            f"**WA {get_status(tomorrow_wa, washington_target)}**"
        )
        
        st.write(
            f"10-12: {counts['washington']['tomorrow']['10-12']}"
        )
        
        st.write(
            f"1-3: {counts['washington']['tomorrow']['1-3']}"
        )
        
        st.write(
            f"4-6: {counts['washington']['tomorrow']['4-6']}"
        )
        
        st.markdown(
            f"**CA {get_status(tomorrow_ca, socal_target)}**"
        )
        
        st.write(
            f"10-12: {counts['socal']['tomorrow']['10-12']}"
        )
        
        st.write(
            f"1-3: {counts['socal']['tomorrow']['1-3']}"
        )
        
        st.write(
            f"4-6: {counts['socal']['tomorrow']['4-6']}"
        )
