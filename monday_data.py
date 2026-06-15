import requests
from datetime import datetime, timedelta
from collections import defaultdict

def load_monday_data():

    import time
    start_time = time.time()

    import streamlit as st

    API_TOKEN = st.secrets["MONDAY_API_KEY"]
    BOARD_ID = 1962914669


    headers = {
        "Authorization": API_TOKEN
    }

    all_items = []

    # First page
    
    today = datetime.now().strftime("%Y-%m-%d")

    query = f"""
    {{
        boards(ids: {BOARD_ID}) {{
            items_page(
                limit: 500,
                query_params: {{
                    rules: [
                        {{
                            column_id: "date_mkr2q53p",
                            compare_value: ["{today}"],
                            operator: greater_than_or_equals
                        }}
                    ]
                }}
            ) {{
                cursor
                items {{
                    name
                    column_values {{
                        id
                        text
                    }}
                }}
            }}
        }}
    }}
    """

    response = requests.post(
    "https://api.monday.com/v2",
    json={"query": query},
    headers=headers
    )

    data = response.json()

    page = data["data"]["boards"][0]["items_page"]

    all_items.extend(page["items"])

    cursor = None

    while False:
        
        today_date = datetime.now().date()
        ...
        print(f"AFTER FILTER: {len(all_items)}")    # Remaining pages

    print()
    print(f"TOTAL ITEMS LOADED: {len(all_items)}")
    print()

    today = datetime.now().strftime("%Y-%m-%d")

    print(f"TODAY = {today}")
    print("=" * 100)

    print()
    print(f"TOTAL ITEMS LOADED: {len(all_items)}")
    print()

    today = datetime.now().strftime("%Y-%m-%d")

    print(f"TODAY = {today}")
    print("=" * 100)

    seen = set()

    today_counts = {
        "10AM-1PM": defaultdict(int),
        "1PM-4PM": defaultdict(int),
        "4PM-7PM": defaultdict(int),
        "7PM-8PM": defaultdict(int)
    }

    tomorrow_counts = {
        "10AM-1PM": defaultdict(int),
        "1PM-4PM": defaultdict(int),
        "4PM-7PM": defaultdict(int),
        "7PM-8PM": defaultdict(int)
    }

    universal_today = {
        "10AM-1PM": defaultdict(int),
        "1PM-4PM": defaultdict(int),
        "4PM-7PM": defaultdict(int),
        "7PM-8PM": defaultdict(int)
    }

    universal_tomorrow = {
        "10AM-1PM": defaultdict(int),
        "1PM-4PM": defaultdict(int),
        "4PM-7PM": defaultdict(int),
        "7PM-8PM": defaultdict(int)
    }

    mccormick_today = {
        "10AM-1PM": defaultdict(int),
        "1PM-4PM": defaultdict(int),
        "4PM-7PM": defaultdict(int),
        "7PM-8PM": defaultdict(int)
    }

    mccormick_tomorrow = {
        "10AM-1PM": defaultdict(int),
        "1PM-4PM": defaultdict(int),
        "4PM-7PM": defaultdict(int),
        "7PM-8PM": defaultdict(int)
    }

    safegreen_today = {
        "10AM-1PM": defaultdict(int),
        "1PM-4PM": defaultdict(int),
        "4PM-7PM": defaultdict(int),
        "7PM-8PM": defaultdict(int)
    }

    safegreen_tomorrow = {
        "10AM-1PM": defaultdict(int),
        "1PM-4PM": defaultdict(int),
        "4PM-7PM": defaultdict(int),
        "7PM-8PM": defaultdict(int)
    }

    nova_today = {
        "10AM-1PM": defaultdict(int),
        "1PM-4PM": defaultdict(int),
        "4PM-7PM": defaultdict(int),
        "7PM-8PM": defaultdict(int)
    }

    nova_tomorrow = {
        "10AM-1PM": defaultdict(int),
        "1PM-4PM": defaultdict(int),
        "4PM-7PM": defaultdict(int),
        "7PM-8PM": defaultdict(int)
    }

    seen = set()

    today_date = datetime.now().date()

    if today_date.weekday() == 4:
        tomorrow_date = today_date + timedelta(days=2)

    elif today_date.weekday() == 5:
        tomorrow_date = today_date + timedelta(days=1)

    else:
        tomorrow_date = today_date + timedelta(days=1)


    # ONLY KEEP APPOINTMENTS FOR TODAY OR TOMORROW
    filtered_items = []

    for item in all_items:

        meeting_date = ""

        for col in item["column_values"]:

            if col["id"] == "date_mkr2q53p":
                meeting_date = col["text"]

        if not meeting_date:
            continue

        try:
            dt = datetime.strptime(
                meeting_date,
                "%Y-%m-%d %H:%M"
            )

        except:
            continue

        if dt.date() in [today_date, tomorrow_date]:
            filtered_items.append(item)

    confirmed = 0
    rejected = 0
    cancelled = 0
    reschedule = 0

    tommy_leads = 0
    elite_leads = 0
    universal_leads = 0

    mccormick_leads = 0
    safegreen_leads = 0
    nova_leads = 0

    for item in filtered_items:

        meeting_date = ""
        disburse = ""
        source = ""
        qa_notes = ""

        for col in item["column_values"]:

            if col["id"] == "date_mkr2q53p":
                meeting_date = col["text"]

            elif col["id"] == "status":
                disburse = col["text"]

            elif col["id"] == "text_mkr22s20":
                source = col["text"]

            elif col["id"] == "long_text_mm0cvyan":
                qa_notes = col["text"]

        source_upper = source.upper()
        qa_upper = qa_notes.upper()

        if disburse.upper() == "TOMMY":
            confirmed += 1

            if is_mccormick:
                mccormick_leads += 1

            elif is_nova:
                nova_leads += 1

            elif is_safegreen:
                safegreen_leads += 1

            else:
                tommy_leads += 1

        elif disburse.upper() == "ELITE":
            confirmed += 1
            elite_leads += 1

        elif disburse.upper() == "UNIVERSAL":
            confirmed += 1
            universal_leads += 1

        elif disburse.upper() == "REJECTED":
            rejected += 1

        elif disburse.upper() == "CANCELED":
            cancelled += 1

        elif disburse.upper() == "RESCHEDULE":
            reschedule += 1

        is_mccormick = "MCCORMICK" in source_upper

        is_nova = "NOVA" in source_upper

        is_safegreen = (
            "SAFE & GREEN" in source_upper
            or "KATHLEEN" in source_upper
        )

        is_universal = (
            "ADU LEAD" in qa_upper
            or "SOLAR LEAD" in qa_upper
            or "POOL LEAD" in qa_upper
        )

        if not meeting_date:
            continue

        lead_key = (
            item["name"],
            meeting_date
        )

        if lead_key in seen:
            continue

        seen.add(lead_key)

        try:
            dt = datetime.strptime(
                meeting_date,
                "%Y-%m-%d %H:%M"
            )

        except:
            continue

        state = None

        if "OREGON" in source_upper:
            state = "OR"

        elif "WASHINGTON" in source_upper:
            state = "WA"

        elif "CALIFORNIA" in source_upper:
            state = "CA"

        if not state:
            continue

        hour = dt.hour

        if hour < 13:
            slot = "10AM-1PM"

        elif hour < 16:
            slot = "1PM-4PM"

        elif hour < 19:
            slot = "4PM-7PM"

        else:
            slot = "7PM-8PM"

        if disburse.upper() not in ["CANCELED", "REJECTED"]:

            if is_universal:

                if dt.date() == today_date:
                    universal_today[slot][state] += 1

                elif dt.date() == tomorrow_date:
                    universal_tomorrow[slot][state] += 1

            elif is_mccormick:

                if dt.date() == today_date:
                    mccormick_today[slot][state] += 1

                elif dt.date() == tomorrow_date:
                    mccormick_tomorrow[slot][state] += 1

            elif is_safegreen:

                if dt.date() == today_date:
                    safegreen_today[slot][state] += 1

                elif dt.date() == tomorrow_date:
                    safegreen_tomorrow[slot][state] += 1

            elif is_nova:

                if dt.date() == today_date:
                    nova_today[slot][state] += 1

                elif dt.date() == tomorrow_date:
                    nova_tomorrow[slot][state] += 1

            else:

                if dt.date() == today_date:
                    today_counts[slot][state] += 1

                elif dt.date() == tomorrow_date:
                    tomorrow_counts[slot][state] += 1
    print()            
    print(f"Runtime: {time.time() - start_time:.2f} seconds")

    print("========== FINAL COUNTS ==========")
    print("confirmed =", confirmed)
    print("rejected =", rejected)
    print("cancelled =", cancelled)
    print("reschedule =", reschedule)
    print("tommy_leads =", tommy_leads)
    print("elite_leads =", elite_leads)
    print("universal_leads =", universal_leads)
    print("==================================")

    return (
        today_counts,
        tomorrow_counts,
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
    )
