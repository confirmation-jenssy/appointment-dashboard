# ==============================
# FILE: dashboard (4).py 
# ==============================

import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

from monday_api import BOARD_ID, get_monday_items, get_report_items

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
        "Total Appointment"
    ]
)

if st.sidebar.button("🔄 Refresh Data"):
    get_monday_items.clear()
    get_report_items.clear()
    st.rerun()

if page == "End of Day Report":

    st.title("📋 End of Day Report")

    today_default = datetime.now(ZoneInfo("America/Los_Angeles")).date()

    selected_date = st.date_input(
        "Report Date",
        value=today_default,
        max_value=today_default
    )

    if selected_date == today_default:
        report_items = get_monday_items()
    else:
        report_items = get_report_items(selected_date)

    st.caption(f"{len(report_items)} item(s) fetched from Monday.com for {selected_date.strftime('%m/%d/%Y')}.")

    CLIENT_COLORS = {
        "tommy": "#2563eb",
        "elite": "#7c3aed",
        "universal": "#d97706",
        "mccormick": "#dc2626",
        "nova": "#db2777",
    }

    def confirm_card(label, color, confirmed, confirm_pct):
        st.markdown(
            f"<h4 style='color:{color}; margin-bottom:4px;'>{label}</h4>",
            unsafe_allow_html=True
        )
        st.metric("Confirmed", confirmed)
        st.metric("Confirm %", f"{confirm_pct}%")
        st.progress(min(1.0, confirm_pct / 100))

    def breakdown_row(report, label=None):
        if label:
            st.markdown(f"**Not Confirmed — {label}**")
        else:
            st.markdown("**Not Confirmed**")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("No Answer", report["no_answer"])
        c2.metric("Cancelled", report["cancelled"])
        c3.metric("Reschedule", report["reschedule"])
        c4.metric("Rejected", report["rejected"])

    with st.container():

        tab1, tab2 = st.tabs([
            "Tommy, Elite & Universal",
            "Nova & McCormick"
        ])

        if report_items:

            with tab1:

                report = build_tommy_elite_report(report_items, selected_date)
                universal_report = build_universal_report(report_items, selected_date)

                # Same pool: Tommy + Elite + Universal combined
                pool_confirmed = report["confirmed"] + universal_report["confirmed"]
                pool_total_leads = report["total_leads"] + universal_report["total_leads"]
                pool_same_day = report["same_day"] + universal_report["same_day"]

                pool_conversion = round(
                    (pool_confirmed / max(1, pool_total_leads)) * 100, 2
                )
                pool_same_day_percent = round(
                    (pool_same_day / max(1, pool_confirmed)) * 100, 2
                )

                pool_report = {
                    "no_answer": report["no_answer"] + universal_report["no_answer"],
                    "cancelled": report["cancelled"] + universal_report["cancelled"],
                    "reschedule": report["reschedule"] + universal_report["reschedule"],
                    "rejected": report["rejected"] + universal_report["rejected"],
                }

                with st.container(border=True):

                    st.markdown(
                        "<h4 style='margin-bottom:4px;'>Overall — Tommy, Elite & Universal</h4>",
                        unsafe_allow_html=True
                    )

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Confirmed", pool_confirmed)
                    c2.metric("Confirm %", f'{pool_conversion}%')
                    c3.metric("Same Day", pool_same_day)
                    c4.metric("Same Day %", f'{pool_same_day_percent}%')

                    st.progress(min(1.0, pool_conversion / 100))

                st.write("")

                c1, c2, c3 = st.columns(3)

                with c1:
                    with st.container(border=True):
                        confirm_card(
                            "Tommy",
                            CLIENT_COLORS["tommy"],
                            report["tommy"],
                            round((report["tommy"] / max(1, pool_confirmed)) * 100, 1)
                        )

                with c2:
                    with st.container(border=True):
                        confirm_card(
                            "Elite",
                            CLIENT_COLORS["elite"],
                            report["elite"],
                            round((report["elite"] / max(1, pool_confirmed)) * 100, 1)
                        )

                with c3:
                    with st.container(border=True):
                        confirm_card(
                            "Universal",
                            CLIENT_COLORS["universal"],
                            universal_report["confirmed"],
                            round((universal_report["confirmed"] / max(1, pool_confirmed)) * 100, 1)
                        )

                st.write("")

                with st.container(border=True):
                    breakdown_row(pool_report, label="Tommy, Elite & Universal")

            with tab2:

                nova_report = build_nova_report(report_items, selected_date)
                mccormick_report = build_mccormick_report(report_items, selected_date)

                # Same pool: Nova + McCormick combined
                pool_confirmed = nova_report["confirmed"] + mccormick_report["confirmed"]
                pool_total_leads = nova_report["total_leads"] + mccormick_report["total_leads"]
                pool_same_day = nova_report["same_day"] + mccormick_report["same_day"]

                pool_conversion = round(
                    (pool_confirmed / max(1, pool_total_leads)) * 100, 2
                )
                pool_same_day_percent = round(
                    (pool_same_day / max(1, pool_confirmed)) * 100, 2
                )

                pool_report = {
                    "no_answer": nova_report["no_answer"] + mccormick_report["no_answer"],
                    "cancelled": nova_report["cancelled"] + mccormick_report["cancelled"],
                    "reschedule": nova_report["reschedule"] + mccormick_report["reschedule"],
                    "rejected": nova_report["rejected"] + mccormick_report["rejected"],
                }

                with st.container(border=True):

                    st.markdown(
                        "<h4 style='margin-bottom:4px;'>Overall — Nova & McCormick</h4>",
                        unsafe_allow_html=True
                    )

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Confirmed", pool_confirmed)
                    c2.metric("Confirm %", f'{pool_conversion}%')
                    c3.metric("Same Day", pool_same_day)
                    c4.metric("Same Day %", f'{pool_same_day_percent}%')

                    st.progress(min(1.0, pool_conversion / 100))

                st.write("")

                c1, c2 = st.columns(2)

                with c1:
                    with st.container(border=True):
                        confirm_card(
                            "Nova",
                            CLIENT_COLORS["nova"],
                            nova_report["confirmed"],
                            round((nova_report["confirmed"] / max(1, pool_confirmed)) * 100, 1)
                        )

                with c2:
                    with st.container(border=True):
                        confirm_card(
                            "McCormick",
                            CLIENT_COLORS["mccormick"],
                            mccormick_report["confirmed"],
                            round((mccormick_report["confirmed"] / max(1, pool_confirmed)) * 100, 1)
                        )

                st.write("")

                with st.container(border=True):
                    breakdown_row(pool_report, label="Nova & McCormick")

        else:
            st.info(f"No leads found for {selected_date.strftime('%m/%d/%Y')}.")

if page == "Total Appointment":

    st.title("📅 Total Appointment")

    counts = build_appointment_counts(items)

    STATE_INFO = {
        "oregon": {"label": "Oregon", "abbr": "OR", "color": "#2563eb", "emoji": "🔵"},
        "washington": {"label": "Washington", "abbr": "WA", "color": "#16a34a", "emoji": "🟢"},
        "socal": {"label": "Southern California", "abbr": "CA", "color": "#dc2626", "emoji": "🔴"},
    }

    SLOT_LABELS = {
        "10-12": "10AM–12PM",
        "1-3": "1PM–3PM",
        "4-6": "4PM–6PM",
        "7-8": "7PM–8PM",
    }

    def get_slot_status(booked, target):
        if booked == 0:
            return "🔴 Empty"
        elif booked < target:
            return "🟡 Needs Leads"
        elif booked == target:
            return "🟢 Goal Met"
        return "🔵 Extra Leads"

    # ------------------------------------------------------------------
    # SETTINGS — reps per state + confirmation rate
    # ------------------------------------------------------------------
    with st.container(border=True):

        st.subheader("⚙️ Settings")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"<span style='color:{STATE_INFO['oregon']['color']};font-weight:bold'>OR Reps</span>",
                unsafe_allow_html=True
            )
            oregon_reps = st.number_input(
                "OR Reps", min_value=0, value=2, label_visibility="collapsed"
            )

        with c2:
            st.markdown(
                f"<span style='color:{STATE_INFO['washington']['color']};font-weight:bold'>WA Reps</span>",
                unsafe_allow_html=True
            )
            washington_reps = st.number_input(
                "WA Reps", min_value=0, value=2, label_visibility="collapsed"
            )

        with c3:
            st.markdown(
                f"<span style='color:{STATE_INFO['socal']['color']};font-weight:bold'>CA Reps</span>",
                unsafe_allow_html=True
            )
            socal_reps = st.number_input(
                "CA Reps", min_value=0, value=2, label_visibility="collapsed"
            )

        with c4:
            st.markdown("**Confirmation Rate %**")
            confirmation_rate = st.number_input(
                "Confirmation Rate %",
                min_value=1, max_value=100, value=50,
                label_visibility="collapsed"
            )

        st.caption(
            f"Confirmation rate only applies to **Tomorrow** — same-day leads are booked "
            f"hot and treated as 100% confirmed."
        )

    lead_multiplier = 100 / confirmation_rate

    # Raw booking capacity per rep - no adjustment. Same-day appointments are
    # booked by the team and are effectively already confirmed (100% show
    # rate), so today's goals use this raw number directly.
    capacity = {
        "oregon": oregon_reps * 3,
        "washington": washington_reps * 3,
        "socal": socal_reps * 3,
    }

    reps = {
        "oregon": oregon_reps,
        "washington": washington_reps,
        "socal": socal_reps,
    }

    # Tomorrow's appointments are set in advance, so some won't confirm
    # (no answer, cancel, etc). These targets are inflated by the
    # confirmation rate so hitting them actually yields the raw capacity
    # in confirmed appointments.
    target = {
        state: round(cap * lead_multiplier)
        for state, cap in capacity.items()
    }

    # ------------------------------------------------------------------
    # HEADLINE METRICS
    # ------------------------------------------------------------------
    st.write("")
    m1, m2, m3 = st.columns(3)

    for col, state in zip((m1, m2, m3), ("oregon", "washington", "socal")):
        info = STATE_INFO[state]
        with col:
            st.markdown(
                f"<h4 style='color:{info['color']}; margin-bottom:0;'>{info['emoji']} {info['abbr']}</h4>",
                unsafe_allow_html=True
            )
            st.metric(
                "Reps Can Book",
                capacity[state],
                delta=f"{reps[state]} reps",
                delta_color="off"
            )

    st.divider()

    def total_for(state, day):
        day_counts = counts[state][day]
        return day_counts["10-12"] + day_counts["1-3"] + day_counts["4-6"]

    today_total = sum(total_for(s, "today") for s in STATE_INFO)
    tomorrow_total = sum(total_for(s, "tomorrow") for s in STATE_INFO)

    tt1, tt2 = st.columns(2)
    tt1.metric("📌 Same Day Appointments Booked", today_total)
    tt2.metric("📆 Tomorrow Appointments Booked", tomorrow_total)

    st.divider()

    # ------------------------------------------------------------------
    # RENDER ONE STATE'S SLOT BREAKDOWN
    # ------------------------------------------------------------------
    def render_state_block(state, day, slot_target):

        info = STATE_INFO[state]
        day_counts = counts[state][day]

        booked_total = day_counts["10-12"] + day_counts["1-3"] + day_counts["4-6"] + day_counts["7-8"]
        goal_total = slot_target * 4

        st.markdown(
            f"<h4 style='color:{info['color']}; margin-bottom:4px;'>{info['emoji']} {info['label']}</h4>",
            unsafe_allow_html=True
        )

        progress = 0.0 if goal_total == 0 else min(1.0, booked_total / goal_total)
        st.progress(progress)
        st.caption(f"{booked_total} / {goal_total} leads booked toward goal")

        slot_cols = st.columns(4)
        needs = []

        for col, (slot_key, slot_label) in zip(slot_cols, SLOT_LABELS.items()):

            booked = day_counts[slot_key]

            with col:
                st.metric(slot_label, booked, delta=f"Goal {slot_target}", delta_color="off")
                st.caption(get_slot_status(booked, slot_target))

            missing = max(0, slot_target - booked)
            if missing:
                needs.append(f"{slot_label} → **{missing} more**")

        if needs:
            st.warning("Needs Leads: " + "  |  ".join(needs))
        else:
            st.success("All slots at or above goal ✅")

        st.divider()

    # ------------------------------------------------------------------
    # TABS: SAME DAY vs TOMORROW
    # ------------------------------------------------------------------
    tab_today, tab_tomorrow = st.tabs([
        "📌 Same Day Appt Needed",
        "📆 Tomorrow"
    ])

    with tab_today:

        st.caption(
            "Same-day leads are booked hot by the team and count as 100% "
            "confirmed — goal is the raw rep capacity, no buffer applied."
        )

        for state in ("oregon", "washington", "socal"):
            slot_target = round(capacity[state] / 3)
            render_state_block(state, "today", slot_target)

    with tab_tomorrow:

        st.caption(
            f"Tomorrow's leads aren't guaranteed to confirm, so goals are "
            f"inflated using the {confirmation_rate}% confirmation rate above "
            f"to cover no-answers and cancellations."
        )

        for state in ("oregon", "washington", "socal"):
            slot_target = round(target[state] / 3)
            render_state_block(state, "tomorrow", slot_target)


def get_column_value(item, column_id):

    for col in item["column_values"]:

        if col["id"] == column_id:
            return col.get("text", "")

    return ""
