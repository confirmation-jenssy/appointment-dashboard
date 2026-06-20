# ==============================
# FILE: reporting (1).py 
# ==============================
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import time # Added for better handling of parsing attempts

LA = ZoneInfo("America/Los_Angeles")

from config import (
    COLUMN_IDS,
    CONFIRMED_STATUSES,
    TOTAL_LEAD_STATUSES
)


def parse_meeting_date(date_string):
    if not date_string:
        return None

    date_formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y"
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(
                date_string,
                fmt
            )
        except ValueError:
            continue

    return None


def build_report(items):

    # ... (rest of report initialization remains the same) ...
    report = {
        "confirmed": 0,
        "same_day": 0,
        "tommy": 0,
        "elite": 0,
        "universal": 0,
        "no_answer": 0,
        "cancelled": 0,
        "reschedule": 0,
        "rejected": 0,
        "mccormick": 0,
        "nova": 0,
        "safegreen": 0,
        "total_leads": 0
    }

    today = datetime.now(
        ZoneInfo("America/Los_Angeles")
    ).date()

    for item in items:

        values = {}

        for col in item["column_values"]:
            values[col["id"]] = col["text"]

        meeting_date = values.get(
            COLUMN_IDS["meeting_date"],
            ""
        )

        # --- CRITICAL CHANGE HERE: Use the robust parser function ---
        dt = parse_meeting_date(meeting_date) 
        if dt is None:
             # This item could not be dated, skip it safely.
             continue
            
        # Check if the date part matches today's date
        if dt.date() != today:
            continue

        raw_status = values.get(
            COLUMN_IDS["status"],
            ""
        )
        
        # ... (The rest of the logic remains the same, as it was correct for counting statuses/sources) ...
        raw_same_day = values.get(
            COLUMN_IDS["same_day"],
            ""
        )
        
        status = raw_status.upper().strip()
        source = values.get(
            COLUMN_IDS["source"],
            ""
        ).upper()
        same_day_status = raw_same_day.upper().strip()
        
        if status in CONFIRMED_STATUSES:

            report["confirmed"] += 1

            if status == "TOMMY":
                report["tommy"] += 1

            elif status == "ELITE":
                report["elite"] += 1

            elif status == "UNIVERSAL":
                report["universal"] += 1

        # ... (rest of the counting logic) ...

        elif status == "NO ANSWER":
            report["no_answer"] += 1

        elif status in ["CANCELED", "CANCELLED"]:
            report["cancelled"] += 1

        elif status == "RESCHEDULE":
            report["reschedule"] += 1

        elif status == "REJECTED":
            report["rejected"] += 1

        if (
            same_day_status == "SAME DAY"
            and status in CONFIRMED_STATUSES
        ):
            report["same_day"] += 1

        if "MCCORMICK" in source:
            report["mccormick"] += 1

        if "NOVA" in source:
            report["nova"] += 1

        if (
            "SAFE & GREEN" in source
            or "KATHLEEN" in source
        ):
            report["safegreen"] += 1

    # ... (The rest of the calculation logic remains the same) ...
    report["total_leads"] = (
        report["confirmed"]
        + report["no_answer"]
        + report["cancelled"]
        + report["reschedule"]
    )

    # Handle division by zero for safety
    report["conversion"] = round(
        (report["confirmed"] /
         max(1, report["total_leads"])) * 100,
        2
    )

    report["same_day_percent"] = round(
        (report["same_day"] /
         max(1, report["confirmed"])) * 100,
        2
    )

    return report


# The helper functions remain unchanged and use the updated build_report
def build_tommy_elite_report(items):
    return build_report(items)

def build_universal_report(items):
    return build_disburse_report(
        items,
        "UNIVERSAL"
    )

def build_mccormick_report(items):
    return build_disburse_report(
        items,
        "MCCORMICK"
    )

def build_nova_report(items):
    return build_disburse_report(
        items,
        "NOVA"
    )

def build_disburse_report(items, client_name):

    report = {
        "confirmed": 0,
        "same_day": 0,
        "no_answer": 0,
        "cancelled": 0,
        "reschedule": 0,
        "rejected": 0,
        "total_leads": 0,
        "conversion": 0
    }

    today = datetime.now(
        ZoneInfo("America/Los_Angeles")
    ).date()

    for item in items:

        values = {}

        for col in item["column_values"]:
            values[col["id"]] = col["text"]

        status = values.get(
            COLUMN_IDS["status"],
            ""
        ).upper().strip()

        if status != client_name.upper():
            continue

        meeting_date = values.get(
            COLUMN_IDS["meeting_date"],
            ""
        )

        dt = parse_meeting_date(meeting_date)

        if dt is None:
            continue

        if dt.date() != today:
            continue

        result = values.get(
            COLUMN_IDS["same_day"],
            ""
        ).upper().strip()

        report["total_leads"] += 1

        if result == "CONFIRMED":
            report["confirmed"] += 1

        elif result == "NO ANSWER":
            report["no_answer"] += 1

        elif result in ["CANCEL", "CANCELED", "CANCELLED"]:
            report["cancelled"] += 1

        elif result == "RESCHEDULE":
            report["reschedule"] += 1

        elif result == "REJECTED":
            report["rejected"] += 1

        elif result == "SAME DAY":
            report["same_day"] += 1
            report["confirmed"] += 1

    report["conversion"] = round(
        (
            report["confirmed"] /
            max(1, report["total_leads"])
        ) * 100,
        2
    )

    return report

def create_campaign_counts():

    return {
        "total": 0,
        "worked": 0,
        "left": 0,
        "today": {
            "10-12": 0,
            "1-3": 0,
            "4-6": 0,
            "7-8": 0
        },
        "tomorrow": {
            "10-12": 0,
            "1-3": 0,
            "4-6": 0,
            "7-8": 0
        }
    }

def add_time_bucket(bucket, hour):

    if 10 <= hour <= 12:
        bucket["10-12"] += 1

    elif 13 <= hour <= 15:
        bucket["1-3"] += 1

    elif 16 <= hour <= 18:
        bucket["4-6"] += 1

    elif 19 <= hour <= 20:
        bucket["7-8"] += 1

def build_appointment_counts(items):

    today = datetime.now(
        ZoneInfo("America/Los_Angeles")
    ).date()
    tomorrow = today + timedelta(days=1)

    counts = {
        "tommy_elite": create_campaign_counts(),
        "mccormick": create_campaign_counts(),
        "nova": create_campaign_counts(),
        "universal": create_campaign_counts()
    }

    for item in items:

        values = {}

        for col in item["column_values"]:
            values[col["id"]] = col["text"]

        source = values.get(COLUMN_IDS["source"], "").upper()
        status = values.get(COLUMN_IDS["status"], "").upper().strip()
        confirmation = values.get(COLUMN_IDS["confirmation"], "").strip()

        meeting_date = values.get(COLUMN_IDS["meeting_date"], "")

        dt = parse_meeting_date(meeting_date)

        if dt is None:
            continue

        campaign = None

        if "TOMMY" in source:
            campaign = "tommy_elite"
        elif "MCCORMICK" in source:
            campaign = "mccormick"
        elif "NOVA" in source:
            campaign = "nova"
        elif status == "UNIVERSAL":
            campaign = "universal"

        if campaign is None:
            continue

        appointment_day = dt.date()

        # TODAY DAY
        if appointment_day == today:

            counts[campaign]["total"] += 1

            if confirmation != "":
                counts[campaign]["worked"] += 1
            else:
                add_time_bucket(
                    counts[campaign]["today"],
                    dt.hour
                )
        # TOMORRROW COUNTS
        elif appointment_day == tomorrow:

            if confirmation == "":
                add_time_bucket(
                    counts[campaign]["tomorrow"],
                    dt.hour
                )
    
    for campaign in counts.values():

        campaign["left"] = (
            campaign["total"]
            - campaign["worked"]
        )

    counts["debug"] = {
        "today": str(today),
        "tomorrow": str(tomorrow),
        "today_count": (
            counts["tommy_elite"]["total"]
            + counts["mccormick"]["total"]
            + counts["nova"]["total"]
            + counts["universal"]["total"]
            )
    }
    
    return counts
