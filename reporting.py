from datetime import datetime

from config import (
    COLUMN_IDS,
    CONFIRMED_STATUSES,
    TOTAL_LEAD_STATUSES
)


def build_report(items):

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

        if not meeting_date:
            continue

        try:
            dt = datetime.strptime(
                meeting_date,
                "%Y-%m-%d %H:%M"
            )
        except:
            continue

        if dt.date() != today:
            continue

        raw_status = values.get(
            COLUMN_IDS["status"],
            ""
        )
        
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
        
        print(
            item["name"],
            "| STATUS =",
            repr(raw_status)
        )
        
        print(
            item["name"],
            "| SAME DAY =",
            repr(raw_same_day)
        )
        
        print(
            item["name"],
            "| SOURCE =",
            repr(source)
        )

        if status in CONFIRMED_STATUSES:

            report["confirmed"] += 1

            if status == "TOMMY":
                report["tommy"] += 1

            elif status == "ELITE":
                report["elite"] += 1

            elif status == "UNIVERSAL":
                report["universal"] += 1

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

    report["total_leads"] = (
        report["confirmed"]
        + report["no_answer"]
        + report["cancelled"]
        + report["reschedule"]
    )

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
