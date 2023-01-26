import datetime
import json
import logging
import os
# import sys

import requests
# import pwinput
# import readchar
import zipfile

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

# Configure debug logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables if defined
email = os.getenv("garmin_email")
password = os.getenv("garmin_password")
api = None

# Example selections and settings
today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)  # Select past week
start = 0
limit = 100
start_badge = 1  # Badge related calls calls start counting at 1
activitytype = ""  # Possible values are: cycling, running, swimming, multi_sport, fitness_equipment, hiking,
# walking, other
activityfile = "MY_ACTIVITY.fit"  # Supported file types are: .fit .gpx .tcx


def display_json(api_call, output):
    """Format API output for better readability."""

    dashed = "-" * 20
    header = f"{dashed} {api_call} {dashed}"
    footer = "-" * len(header)

    print(header)
    print(json.dumps(output, indent=4))
    print(footer)


def display_text(output):
    """Format API output for better readability."""

    dashed = "-" * 60
    header = f"{dashed}"
    footer = "-" * len(header)

    print(header)
    print(json.dumps(output, indent=4))
    print(footer)


def get_credentials():
    global email, password
    #    """Get user credentials."""
    #    email = input("Login e-mail: ")
    #    password = pwinput.pwinput(prompt='Password: ')
    return email, password


def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    try:
        # Try to load the previous session
        with open("session.json") as f:
            saved_session = json.load(f)

            print(
                "Login to Garmin Connect using session loaded from 'session.json'...\n"
            )

            # Use the loaded session for initializing the API (without need for credentials)
            api = Garmin(session_data=saved_session)

            # Login using the
            api.login()

    except (FileNotFoundError, GarminConnectAuthenticationError):
        # Login to Garmin Connect portal with credentials since session is invalid or not present.
        print(
            "Session file not present or turned invalid, login with your Garmin Connect credentials.\n"
            "NOTE: Credentials will not be stored, the session cookies will be stored in 'session.json' for future use.\n"
        )
        try:
            # Ask for credentials if not set as environment variables
            if not email or not password:
                email, password = get_credentials()

            api = Garmin(email, password)
            api.login()

            # Save session dictionary to json file for future use
            with open("session.json", "w", encoding="utf-8") as f:
                json.dump(api.session_data, f, ensure_ascii=False, indent=4)
        except (
                GarminConnectConnectionError,
                GarminConnectAuthenticationError,
                GarminConnectTooManyRequestsError,
                requests.exceptions.HTTPError,
        ) as err:
            logger.error("Error occurred during Garmin Connect communication: %s", err)
            return None

    return api


def get_last_activity(api=None):
    if not api:
        api = init_api(email, password)

    fit_file_name = '10241888920_ACTIVITY.fit'
    # Get last activity
    last_activity = api.get_last_activity()
    return api, last_activity


def download_activity(api, activity_id):
    print(f"api.download_activity({activity_id}, dl_fmt=api.ActivityDownloadFormat.ORIGINAL)")
    zip_data = api.download_activity(
        activity_id, dl_fmt=api.ActivityDownloadFormat.ORIGINAL
    )
    output_file = f"./{str(activity_id)}.zip"
    with open(output_file, "wb") as fb:
        fb.write(zip_data)
    print(f"Activity data downloaded to file {output_file}")

    with zipfile.ZipFile('./' + str(activity_id) + '.zip', 'r') as zip_ref:
        zip_ref.extractall('./')
    return str(activity_id) + '_ACTIVITY.fit'

# for i in range(10):
#     # Init API
#     if not api:
#         api = init_api(email, password)
#     else:
#         break
#
# api, last_activity = get_last_activity(api)
# activity_id = last_activity["activityId"]
# fit_file_name = download_activity(api,activity_id)
# print(fit_file_name)
