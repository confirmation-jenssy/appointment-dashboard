from monday_data import load_monday_data
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

def load_reports():

    if not os.path.exists("reports.json"):

        return {
            "daily": {},
            "weekly": {},
            "monthly": {}
        }

    with open("reports.json", "r") as f:

        return json.load(f)


def save_reports(data):

    with open("reports.json", "w") as f:

        json.dump(data, f, indent=4)

st.set_page_config(page_title="OUTSOURCE ENGAGE CONFIRMATION", layout="wide")

page = st.sidebar.radio("Navigation", ["Home", "Confirmation Reports"])

if page == "Home":

    (
        today_slots,
        tomorrow_slots,
        universal_today,
        universal_tomorrow,
        mccormick_today,
        mccormick_tomorrow,
        safegreen_today,
        safegreen_tomorrow,
        nova_today,
        nova_tomorrow,
        confirmed,
        rejected,
        cancelled,
        reschedule,
        tommy_leads,
        elite_leads,
        universal_leads,
        mccormick_leads,
        safegreen_leads,
        nova_leads
    ) = load_monday_data()

    st.title("📅 OUTSOURCE ENGAGE CONFIRMATION 📅")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Tommy & Elite",
        "Universal",
        "McCormick",
        "Safe & Green",
        "Nova"
    ])

    with tab1:
        st.header("Tommy Builder & Elite Builder Campaign")

        col_today, col_tomorrow = st.columns(2)

        with col_today:
            st.subheader("TODAY")

            for slot, states in today_slots.items():

                st.write(f"### {slot}")

                c1, c2, c3 = st.columns(3)

                c1.metric("CA", states["CA"])
                c2.metric("OR", states["OR"])
                c3.metric("WA", states["WA"])

        with col_tomorrow:
            
            st.subheader("TOMORROW")

            for slot, states in tomorrow_slots.items():

                st.write(f"### {slot}")

                c1, c2, c3 = st.columns(3)

                c1.metric("CA", states["CA"])
                c2.metric("OR", states["OR"])
                c3.metric("WA", states["WA"])

    with tab2:
        st.header("Universal Group Tech Campaign")

        col_today, col_tomorrow = st.columns(2)

        with col_today:
            st.subheader("TODAY")

        for slot, states in universal_today.items():

            st.write(f"### {slot}")

            c1, c2, c3 = st.columns(3)

            c1.metric("CA", states["CA"])
            c2.metric("OR", states["OR"])
            c3.metric("WA", states["WA"])

        st.divider()

        with col_tomorrow:
            st.subheader("TOMORROW")

        for slot, states in universal_tomorrow.items():

            st.write(f"### {slot}")

            c1, c2, c3 = st.columns(3)

            c1.metric("CA", states["CA"])
            c2.metric("OR", states["OR"])
            c3.metric("WA", states["WA"])

    with tab3:
        st.header("McCormick Campaign")   

        col_today, col_tomorrow = st.columns(2)

        with col_today:
            st.subheader("TODAY")

        for slot, states in mccormick_today.items():

            st.write(f"### {slot}")

            c1, c2, c3 = st.columns(3)

            c1.metric("CA", states["CA"])
            c2.metric("OR", states["OR"])
            c3.metric("WA", states["WA"])

        st.divider()

        with col_tomorrow:
            st.subheader("TOMORROW")

        for slot, states in mccormick_tomorrow.items():

            st.write(f"### {slot}")

            c1, c2, c3 = st.columns(3)

            c1.metric("CA", states["CA"])
            c2.metric("OR", states["OR"])
            c3.metric("WA", states["WA"])

    with tab4:
        st.header("Safe & Green Campaign")  

        col_today, col_tomorrow = st.columns(2)

        with col_today:
            st.subheader("TODAY")

        for slot, states in safegreen_today.items():

            st.write(f"### {slot}")

            c1, c2, c3 = st.columns(3)

            c1.metric("CA", states["CA"])
            c2.metric("OR", states["OR"])
            c3.metric("WA", states["WA"])

        st.divider()

        with col_tomorrow:
            st.subheader("TOMORROW")

        for slot, states in safegreen_tomorrow.items():

            st.write(f"### {slot}")

            c1, c2, c3 = st.columns(3)

            c1.metric("CA", states["CA"])
            c2.metric("OR", states["OR"])
            c3.metric("WA", states["WA"])

    with tab5:
        st.header("Nova Campaign")         

        col_today, col_tomorrow = st.columns(2)

        with col_today:
            st.subheader("TODAY")

        for slot, states in nova_today.items():

            st.write(f"### {slot}")

            c1, c2, c3 = st.columns(3)

            c1.metric("CA", states["CA"])
            c2.metric("OR", states["OR"])
            c3.metric("WA", states["WA"])

        st.divider()

        with col_tomorrow:
            st.subheader("TOMORROW")

        for slot, states in nova_tomorrow.items():

            st.write(f"### {slot}")

            c1, c2, c3 = st.columns(3)

            c1.metric("CA", states["CA"])
            c2.metric("OR", states["OR"])
            c3.metric("WA", states["WA"]) 

    today_weekday = datetime.now().weekday()

    st.divider()

    st.header("🎯 Goals")

    c1, c2, c3 = st.columns(3)

    daily_leads = 0
    weekly_leads = 0
    monthly_leads = 0

    c1.metric(
    "Daily Goal",
    f"{daily_leads} / 50"
    )

    c2.metric(
    "Weekly Goal",
    f"{weekly_leads} / 150"
    )

    c3.metric(
    "Monthly Goal",
    f"{monthly_leads} / 600"
    )

elif page == "Confirmation Reports":
    st.title("📊 Confirmation Reports")

    (
        today_slots,
        tomorrow_slots,
        universal_today,
        universal_tomorrow,
        mccormick_today,
        mccormick_tomorrow,
        safegreen_today,
        safegreen_tomorrow,
        nova_today,
        nova_tomorrow,
        confirmed,
        rejected,
        cancelled,
        reschedule,
        tommy_leads,
        elite_leads,
        universal_leads,
        mccormick_leads,
        safegreen_leads,
        nova_leads
    ) = load_monday_data()

    reports = load_reports()

    if st.button("🔄 Update Confirmation EOD"):

        today = datetime.now().strftime("%m/%d/%Y")

        total_leads = (
            confirmed +
            rejected +
            cancelled +
            reschedule
        )

        reports["daily"][today] = {

            "Total Leads": total_leads,

            "Confirmed": confirmed,

            "Conversion": f"{round((confirmed / max(1, total_leads)) * 100, 2)}%",

            "Tommy": tommy_leads,
            "Elite": elite_leads,
            "Universal": universal_leads,

            "McCormick": mccormick_leads,
            "Safe & Green": safegreen_leads,
            "Nova": nova_leads,

            "No Answer": 0,
            "Rejected": rejected,
            "Cancelled": cancelled,
            "Reschedule": reschedule
        }

        save_reports(reports)

        st.success(f"Report saved for {today}")

    daily_reports = reports["daily"]

    available_dates = sorted(
        daily_reports.keys(),
        reverse=True
    )

    selected_day = st.selectbox(
        "🔎 Search Historical Reports",
        available_dates
    )

    report = daily_reports[selected_day]

    st.header(f"Daily Report - {selected_day}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Leads", report["Total Leads"])
    c2.metric("Confirmed", report["Confirmed"])
    c3.metric("Conversion", report["Conversion"])

    if report["Total Leads"] > 0:

        progress = 0

        if report["Total Leads"] > 0:
            progress = min(
                    report["Confirmed"] / max(1, report["Total Leads"]),
                    1.0
            )

            st.progress(progress)

    else:

        st.progress(0)

    st.subheader("Lead Breakdown")

    c1, c2, c3 = st.columns(3)
    c1.metric("Tommy", report["Tommy"])
    c2.metric("Elite", report["Elite"])
    c3.metric("Universal", report["Universal"])

    st.subheader("Unconfirmed Outcomes")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("No Answer", report["No Answer"])
    c2.metric("Rejected", report["Rejected"])
    c3.metric("Cancelled", report["Cancelled"])
    c4.metric("Reschedule", report["Reschedule"])

    st.divider()

    st.header("Weekly Report")

    weekly_reports = {

        "Jun 1 - Jun 7": {
            "Leads": 316,
            "Confirmed": 152,
            "Conversion": "48.10%"
        },

        "Jun 8 - Jun 14": {
            "Leads": 272,
            "Confirmed": 159,
            "Conversion": "58.46%"
        }
    }

    selected_week = st.selectbox(
        "Select Week",
        list(weekly_reports.keys())
    )

    week = weekly_reports[selected_week]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Weekly Leads",
        week["Leads"]
    )

    c2.metric(
        "Weekly Confirmed",
        week["Confirmed"]
    )

    c3.metric(
        "Weekly Conversion",
        week["Conversion"]
    )

    st.divider()

    st.header("Monthly Report")

    st.info("Monthly reporting section coming next.")
