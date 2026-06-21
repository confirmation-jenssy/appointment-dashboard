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

# --- CHANGE HERE: Fetch data when needed (and rely on the caching in monday_api.py) ---
items = get_monday_items() 

page = st.sidebar.selectbox(
    "Select Page",
    [
        "End of Day Report",
        "End of Day Export",
        "Total Appointment"
    ]
)

if page == "End of Day Report":

    st.title("End of Day Report")

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
                c4.metric("Confirm %", f'{report["conversion"]}%')

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
                c2.metric("Confirm %", f'{report["conversion"]}%')
            
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
                c2.metric("Confirm %", f'{report["conversion"]}%')
            
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
                c2.metric("Confirm %", f'{report["conversion"]}%')
            
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

if page == "Total Appointment":

    st.title("Total Appointment")

    counts = build_appointment_counts(items)

    st.header("Total Tommy/Elite Reps")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(
            "<span style='color:#2563eb;font-weight:bold'>OR Reps</span>",
            unsafe_allow_html=True
        )
        oregon_reps = st.number_input(
            "OR Reps",
            min_value=0,
            value=2,
            label_visibility="collapsed"
        )
    
    with c2:
        st.markdown(
            "<span style='color:#16a34a;font-weight:bold'>WA Reps</span>",
            unsafe_allow_html=True
        )
        washington_reps = st.number_input(
            "WA Reps",
            min_value=0,
            value=2,
            label_visibility="collapsed"
        )
    
    with c3:
        st.markdown(
            "<span style='color:#dc2626;font-weight:bold'>CA Reps</span>",
            unsafe_allow_html=True
        )
        socal_reps = st.number_input(
            "CA Reps",
            min_value=0,
            value=2,
            label_visibility="collapsed"
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
    
    st.subheader("Appointment Reps are able to Book")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            "<h4 style='color:#2563eb; margin-bottom:0;'>OR</h4>",
            unsafe_allow_html=True
        )
        st.metric(
            label=" ",
            value=oregon_target,
            delta=f"{oregon_reps} reps"
        )
    
    with c2:
        st.markdown(
            "<h4 style='color:#16a34a; margin-bottom:0;'>WA</h4>",
            unsafe_allow_html=True
        )
        st.metric(
            label=" ",
            value=washington_target,
            delta=f"{washington_reps} reps"
        )
    
    with c3:
        st.markdown(
            "<h4 style='color:#dc2626; margin-bottom:0;'>CA</h4>",
            unsafe_allow_html=True
        )
        st.metric(
            label=" ",
            value=socal_target,
            delta=f"{socal_reps} reps"
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
    
        with c1:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div style="color:#2563eb;font-weight:bold;font-size:20px;">
                        OR
                    </div>
                    <div style="font-size:36px;font-weight:bold;">
                        {today_or}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
        with c2:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div style="color:#16a34a;font-weight:bold;font-size:20px;">
                        WA
                    </div>
                    <div style="font-size:36px;font-weight:bold;">
                        {today_wa}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
        with c3:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div style="color:#dc2626;font-weight:bold;font-size:20px;">
                        CA
                    </div>
                    <div style="font-size:36px;font-weight:bold;">
                        {today_ca}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
        c4.metric("TOTAL", today_total)
    
    with right_col:

        st.subheader("Tomorrow")
    
        c1, c2, c3, c4 = st.columns(4)
    
        with c1:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div style="color:#2563eb;font-weight:bold;font-size:20px;">
                        OR
                    </div>
                    <div style="font-size:36px;font-weight:bold;">
                        {tomorrow_or}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
        with c2:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div style="color:#16a34a;font-weight:bold;font-size:20px;">
                        WA
                    </div>
                    <div style="font-size:36px;font-weight:bold;">
                        {tomorrow_wa}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
        with c3:
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div style="color:#dc2626;font-weight:bold;font-size:20px;">
                        CA
                    </div>
                    <div style="font-size:36px;font-weight:bold;">
                        {tomorrow_ca}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
        c4.metric("TOTAL", tomorrow_total)

    st.divider()

    st.info(
        "🔴 Empty    |    🟡 Needs Leads    |    🟢 Goal Met    |    🔵 Extra Leads"
    )
    
    left_col, right_col = st.columns(2)

    def get_status(booked, capacity):

        if booked < (capacity * 0.75):
            return "🟡 NEED LEADS"
    
        elif booked <= capacity:
            return "🟢 FULL"
    
        return "🔴 OVERBOOKED"

    def get_slot_status(booked, target):

        if booked == 0:
            return "🔴"
    
        elif booked < target:
            return "🟡"
    
        elif booked == target:
            return "🟢"
    
        return "🔵"
    
    with left_col:

        st.subheader("Today")

        or_col, wa_col, ca_col = st.columns(3)

        with or_col:

            st.markdown(
                "<h3 style='color:#2563eb'>OR</h3>",
                unsafe_allow_html=True
            )

            # Oregon slots
            or_today = (
            counts["oregon"]["today"]["10-12"]
            + counts["oregon"]["today"]["1-3"]
            + counts["oregon"]["today"]["4-6"]
        )

            # Oregon Needs Leads
            slot_target = round(
                oregon_target / 3
            )
            
            slot_booked = counts["oregon"]["today"]["10-12"]
            
            st.write(
                f"10AM-12PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )
            
            slot_target = round(
                oregon_target / 3
            )
            
            slot_booked = counts["oregon"]["today"]["1-3"]

            st.write(
                f"1PM-3PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )
            
            slot_target = round(
                oregon_target / 3
            )
            
            slot_booked = counts["oregon"]["today"]["4-6"]

            st.write(
                f"4PM-6PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_booked = counts["oregon"]["today"]["7-8"]

            st.write(
                f"7PM-8PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            needs = []

            missing = max(
                0,
                slot_target - counts["oregon"]["today"]["10-12"]
            )
            if missing:
                needs.append(f"10AM-12PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["oregon"]["today"]["1-3"]
            )
            if missing:
                needs.append(f"1PM-3PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["oregon"]["today"]["4-6"]
            )
            if missing:
                needs.append(f"4PM-6PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["oregon"]["today"]["7-8"]
            )
            if missing:
                needs.append(f"7PM-8PM → {missing}")
            
            if needs:
                st.warning("**Needs ↓**")
            
                for item in needs:
                    st.write(f"• {item}")
            
        with wa_col:

            st.markdown(
                "<h3 style='color:#16a34a'>WA</h3>",
                unsafe_allow_html=True
            )

            # Washington slots
            wa_today = (
            counts["washington"]["today"]["10-12"]
            + counts["washington"]["today"]["1-3"]
            + counts["washington"]["today"]["4-6"]
        )

            # Washington Needs Leads
            slot_target = round(
                washington_target / 3
            )

            slot_booked = counts["washington"]["today"]["10-12"]

            st.write(
                f"10AM-12PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_target = round(
                washington_target / 3
            )

            slot_booked = counts["washington"]["today"]["1-3"]

            st.write(
                f"1PM-3PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_target = round(
                washington_target / 3
            )

            slot_booked = counts["washington"]["today"]["4-6"]

            st.write(
                f"4PM-6PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_booked = counts["washington"]["today"]["7-8"]

            st.write(
                f"7PM-8PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            needs = []

            missing = max(
                0,
                slot_target - counts["washington"]["today"]["10-12"]
            )
            if missing:
                needs.append(f"10AM-12PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["washington"]["today"]["1-3"]
            )
            if missing:
                needs.append(f"1PM-3PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["washington"]["today"]["4-6"]
            )
            if missing:
                needs.append(f"4PM-6PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["washington"]["today"]["7-8"]
            )
            if missing:
                needs.append(f"7PM-8PM → {missing}")
            
            if needs:
                st.warning("**Needs ↓**")
            
                for item in needs:
                    st.write(f"• {item}")

        with ca_col:

            st.markdown(
                "<h3 style='color:#dc2626'>CA</h3>",
                unsafe_allow_html=True
            )

            # California slots
            ca_today = (
            counts["socal"]["today"]["10-12"]
            + counts["socal"]["today"]["1-3"]
            + counts["socal"]["today"]["4-6"]
        )

            # California Needs Leads
            slot_target = round(
                socal_target / 3
            )

            slot_booked = counts["socal"]["today"]["10-12"]

            st.write(
                f"10AM-12PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_target = round(
                socal_target / 3
            )

            slot_booked = counts["socal"]["today"]["1-3"]

            st.write(
                f"1PM-3PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_target = round(
                socal_target / 3
            )

            slot_booked = counts["socal"]["today"]["4-6"]

            st.write(
                f"4PM-6PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_booked = counts["socal"]["today"]["7-8"]

            st.write(
                f"7PM-8PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            needs = []

            missing = max(
                0,
                slot_target - counts["socal"]["today"]["10-12"]
            )
            if missing:
                needs.append(f"10AM-12PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["socal"]["today"]["1-3"]
            )
            if missing:
                needs.append(f"1PM-3PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["socal"]["today"]["4-6"]
            )
            if missing:
                needs.append(f"4PM-6PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["socal"]["today"]["7-8"]
            )
            if missing:
                needs.append(f"7PM-8PM → {missing}")
            
            if needs:
                st.warning("**Needs ↓**")
            
                for item in needs:
                    st.write(f"• {item}")
    
    with right_col:
        
        st.subheader("Tomorrow")

        or_col, wa_col, ca_col = st.columns(3)

        with or_col:

            st.markdown(
                "<h3 style='color:#2563eb'>OR</h3>",
                unsafe_allow_html=True
            )
        
            slot_target = round(
                oregon_target / 3
            )
            
            slot_booked = counts["oregon"]["tomorrow"]["10-12"]

            st.write(
                f"10AM-12PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )
            
            slot_target = round(
                oregon_target / 3
            )
            
            slot_booked = counts["oregon"]["tomorrow"]["1-3"]

            st.write(
                f"1PM-3PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )
            
            slot_target = round(
                oregon_target / 3
            )
            
            slot_booked = counts["oregon"]["tomorrow"]["4-6"]

            st.write(
                f"4PM-6PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_booked = counts["oregon"]["tomorrow"]["7-8"]

            st.write(
                f"7PM-8PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            needs = []

            missing = max(
                0,
                slot_target - counts["oregon"]["tomorrow"]["10-12"]
            )
            if missing:
                needs.append(f"10AM-12PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["oregon"]["tomorrow"]["1-3"]
            )
            if missing:
                needs.append(f"1PM-3PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["oregon"]["tomorrow"]["4-6"]
            )
            if missing:
                needs.append(f"4PM-6PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["oregon"]["tomorrow"]["7-8"]
            )
            if missing:
                needs.append(f"7PM-8PM → {missing}")
            
            if needs:
                st.warning("**Needs ↓**")
            
                for item in needs:
                    st.write(f"• {item}")

        with wa_col:

            st.markdown(
                "<h3 style='color:#16a34a'>WA</h3>",
                unsafe_allow_html=True
            )

            slot_target = round(
            washington_target / 3
        )

            slot_booked = counts["washington"]["tomorrow"]["10-12"]

            st.write(
                f"10AM-12PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_target = round(
                washington_target / 3
            )

            slot_booked = counts["washington"]["tomorrow"]["1-3"]

            st.write(
                f"1PM-3PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_target = round(
                washington_target / 3
            )

            slot_booked = counts["washington"]["tomorrow"]["4-6"]

            st.write(
                f"4PM-6PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_booked = counts["washington"]["tomorrow"]["7-8"]

            st.write(
                f"7PM-8PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            needs = []

            missing = max(
                0,
                slot_target - counts["washington"]["tomorrow"]["10-12"]
            )
            if missing:
                needs.append(f"10AM-12PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["washington"]["tomorrow"]["1-3"]
            )
            if missing:
                needs.append(f"1PM-3PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["washington"]["tomorrow"]["4-6"]
            )
            if missing:
                needs.append(f"4PM-6PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["washington"]["tomorrow"]["7-8"]
            )
            if missing:
                needs.append(f"7PM-8PM → {missing}")
            
            if needs:
                st.warning("**Needs ↓**")
            
                for item in needs:
                    st.write(f"• {item}")    

        with ca_col:

            st.markdown(
                "<h3 style='color:#dc2626'>CA</h3>",
                unsafe_allow_html=True
            )

            slot_target = round(
                socal_target / 3
            )

            slot_booked = counts["socal"]["tomorrow"]["10-12"]

            st.write(
                f"10AM-12PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_target = round(
                socal_target / 3
            )

            slot_booked = counts["socal"]["tomorrow"]["1-3"]

            st.write(
                f"1PM-3PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_target = round(
                washington_target / 3
            )

            slot_booked = counts["socal"]["tomorrow"]["4-6"]

            st.write(
                f"4PM-6PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            slot_booked = counts["socal"]["tomorrow"]["7-8"]

            st.write(
                f"7PM-8PM {get_slot_status(slot_booked, slot_target)}"
            )
            
            st.caption(
                f"Leads: {slot_booked} | Goal: {slot_target}"
            )

            needs = []

            missing = max(
                0,
                slot_target - counts["socal"]["tomorrow"]["10-12"]
            )
            if missing:
                needs.append(f"10AM-12PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["socal"]["tomorrow"]["1-3"]
            )
            if missing:
                needs.append(f"1PM-3PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["socal"]["tomorrow"]["4-6"]
            )
            if missing:
                needs.append(f"4PM-6PM → {missing}")
            
            missing = max(
                0,
                slot_target - counts["socal"]["tomorrow"]["7-8"]
            )
            if missing:
                needs.append(f"7PM-8PM → {missing}")
            
            if needs:
                st.warning("**Needs ↓**")
            
                for item in needs:
                    st.write(f"• {item}")  
        
if page == "End of Day Report":

    st.title("End of Day Report")
        st.subheader("CF Appointments Ready")
    
        st.write("Tommy: 0")
        st.write("Elite: 0")
        st.write("McCormick: 0")
        st.write("Nova: 0")
        st.write("Universal: 0")
    
        st.divider()
    
        st.write("Total: 0")
    
        if st.button("Export CF Appointments"):
            st.success("Export started")
