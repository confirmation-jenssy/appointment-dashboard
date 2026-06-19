# ==============================
# FILE: reporting (1).py 
# ==============================

from datetime import datetime, timedelta
import time # Added for better handling of parsing attempts

from config import (
    COLUMN_IDS,
    CONFIRMED_STATUSES,
    TOTAL_LEAD_STATUSES
)


def parse_meeting_date(date_string):
    """
    Attempts to parse a date string using multiple common formats. 
    Returns the datetime object if successful, otherwise None.
    """
    if not date_string:
        return None

    # List of possible date format codes (YYYY-MM-DD, YYYY-MM-DD HH:MM, etc.)
    date_formats = [
        "%Y-%m-%d %H:%M", # Date and Time (The current expected format)
        "%Y-%m-%d",       # Just the Date
        "%m/%d/%Y",       # Common US Format 
        "%d/%m/%Y"        # Common UK/EU Format
    ]

    for fmt in date_formats:
        try:
            dt = datetime.strptime(date_string, fmt)
            return dt
        except ValueError:
            continue # Try the next format
            
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

    today = datetime.now().date()

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

    today = datetime.now().date()

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

def build_appointment_counts(items):

    counts = {
        "tommy_elite": {
            "total": 25,
            "worked": 18,
            "left": 7,
            "today": {
                "10-12": 0,
                "1-3": 3,
                "4-6": 2,
                "7-8": 2
            },
            "tomorrow": {
                "10-12": 4,
                "1-3": 6,
                "4-6": 3,
                "7-8": 1
            }
        }
    }

    return counts
