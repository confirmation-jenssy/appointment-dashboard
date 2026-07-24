# ==============================
# FILE: monday_api.py
# ==============================

import requests
import streamlit as st
from config import BOARD_ID


@st.cache_data(ttl=60 * 15)  # Cache data for 15 minutes (adjust this time if needed)
def get_monday_items():
    """Fetches and returns items from the Monday board."""
    api_token = st.secrets["MONDAY_API_KEY"]

    headers = {
        "Authorization": api_token
    }

    from datetime import datetime
    from zoneinfo import ZoneInfo

    today = datetime.now(
        ZoneInfo("America/Los_Angeles")
    ).strftime("%Y-%m-%d")

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
                items {{
                    id
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

    try:
        response = requests.post(
            "https://api.monday.com/v2",
            json={"query": query},
            headers=headers
        )
        response.raise_for_status()  # This will raise an exception for bad status codes (4xx or 5xx)

        data = response.json()

        # Check if the required data structure exists before accessing it
        if "data" not in data or "boards" not in data["data"] or not data["data"]["boards"]:
            st.error("Could not find board data on Monday.com.")
            return []  # Return empty list instead of crashing

        return data["data"]["boards"][0]["items_page"]["items"]

    except requests.exceptions.RequestException as e:
        st.error(f"🛑 API Connection Error: Could not connect to Monday.com. Please check your API Key and internet connection. Details: {e}")
        return []  # Return empty list on network failure
    except Exception as e:
        st.error(f"❌ An unexpected error occurred during data fetching: {e}")
        return []


@st.cache_data(ttl=60 * 15)
def get_report_items(selected_date):
    """Fetches items from the Monday board for one specific date (for EOD Report lookback)."""
    api_token = st.secrets["MONDAY_API_KEY"]

    headers = {
        "Authorization": api_token
    }

    date_str = selected_date.strftime("%Y-%m-%d")

    query = f"""
    {{
        boards(ids: {BOARD_ID}) {{
            items_page(
                limit: 500,
                query_params: {{
                    rules: [
                        {{
                            column_id: "date_mkr2q53p",
                            compare_value: ["{date_str}", "{date_str}"],
                            operator: between
                        }}
                    ]
                }}
            ) {{
                items {{
                    id
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

    try:
        response = requests.post(
            "https://api.monday.com/v2",
            json={"query": query},
            headers=headers
        )
        response.raise_for_status()

        data = response.json()

        if "data" not in data or "boards" not in data["data"] or not data["data"]["boards"]:
            st.error("Could not find board data on Monday.com.")
            return []

        return data["data"]["boards"][0]["items_page"]["items"]

    except requests.exceptions.RequestException as e:
        st.error(f"🛑 API Connection Error: Could not connect to Monday.com. Please check your API Key and internet connection. Details: {e}")
        return []
    except Exception as e:
        st.error(f"❌ An unexpected error occurred during data fetching: {e}")
        return []
