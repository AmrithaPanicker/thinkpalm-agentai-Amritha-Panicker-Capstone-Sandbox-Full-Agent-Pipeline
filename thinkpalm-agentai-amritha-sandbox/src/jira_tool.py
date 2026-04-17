import logging
import os
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException, HTTPError, Timeout
from dotenv import load_dotenv

# Optional: Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Load environment variables
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Allow only your tickets (using a Set for faster O(1) lookups)
ALLOWED_TICKETS = {"KAN-10", "KAN-11", "KAN-12", "KAN-13"}


def extract_text(description) -> str:
    """Extracts text from Jira's nested description format securely."""
    # Ensure description is a dictionary before utilizing .get()
    if not isinstance(description, dict):
        return str(description) if description is not None else ""

    text = ""
    try:
        for block in description.get("content", []):
            for inner in block.get("content", []):
                text += inner.get("text", "") + "\n"
    # Avoid bare "except:". Target specifically the errors that might occur on bad nested structures.
    except (TypeError, AttributeError) as getattr_err:
        logging.warning(f"Failed to parse expected description structure: {getattr_err}")
        text = str(description)

    return text.strip()


def fetch_jira_ticket(ticket_id: str) -> str:
    """Fetches a Jira ticket given a ticket ID with comprehensive error handling."""

    # 1. Catch missing environment variables early
    if not all([JIRA_URL, EMAIL, API_TOKEN]):
        return "Configuration Error: Missing one or more Jira environment variables."

    # Restrict to only your tickets
    if ticket_id not in ALLOWED_TICKETS:
        return f"Error: Ticket '{ticket_id}' is not allowed in the system."

    url = f"{JIRA_URL}/rest/api/3/issue/{ticket_id}"

    try:
        # 2. Prevent infinite hangs by always including a timeout
        response = requests.get(
            url,
            auth=HTTPBasicAuth(EMAIL, API_TOKEN),
            headers={"Accept": "application/json"},
            timeout=10 
        )

        # 3. Raise an HTTPError if the status goes off course (4xx or 5xx)
        response.raise_for_status()

        data = response.json()

        # 4. Safely extract nested data utilizing .get() over strict bracket mapping
        fields = data.get("fields", {})
        summary = fields.get("summary", "No Summary Provided")
        description_raw = fields.get("description", "")

        description = extract_text(description_raw)

        return f"{summary}\n\n{description}"

    # --- Error Catching Blocks ---
    except HTTPError as http_err:
        # Handle specific common API failures
        if response.status_code == 401:
            return "Error 401: Unauthorized. Please check your Jira email and API token."
        elif response.status_code == 403:
            return "Error 403: Forbidden. You do not have access to view this ticket."
        elif response.status_code == 404:
            return f"Error 404: Ticket '{ticket_id}' not found."
        else:
            return f"HTTP Error {response.status_code}: {http_err}"

    except Timeout:
        return "Error: The connection to the Jira API timed out."
        
    except requests.exceptions.JSONDecodeError:
        return "Error: The Jira API returned malformed or unexpected data (JSON Decode Error)."

    except RequestException as req_err:
         # Blanket fallback for other network, DNS, connection issues handled by requests
        return f"Network Error occurred: {req_err}"

    except Exception as e:
        # Ultimate fallback
        return f"An unexpected error occurred: {str(e)}"
