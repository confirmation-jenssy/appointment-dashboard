import streamlit as st

from monday_api import get_monday_items
from reporting import (
    build_tommy_elite_report,
    build_universal_report,
    build_mccormick_report,
    build_nova_report
)

st.set_page_config(
    page_title="Confirmation",
    layout="wide"
)

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

    col1, col2 = st.columns([8,1])

    with col2:
        if st.button("🔄 Refresh"):
             st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Tommy & Elite EOD",
        "Universal EOD",
        "McCormick EOD",
        "Nova EOD"
    ])

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

        st.write(report)

    with tab3:

        report = build_mccormick_report(items)

        st.write(report)

    with tab4:

        report = build_nova_report(items)

        st.write(report)
