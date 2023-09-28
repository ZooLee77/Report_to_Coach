import datetime
import json
import logging
import os
# import sys

import requests
# import pwinput
# import readchar
import zipfile
from garth.exc import GarthHTTPError

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
tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
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
        print(
            f"Trying to login to Garmin Connect using token data from '{tokenstore}'...\n"
        )
        garmin = Garmin()
        garmin.login(tokenstore)
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        # Session is expired. You'll need to log in again
        print(
            "Login tokens not present, login with your Garmin Connect credentials to generate them.\n"
            f"They will be stored in '{tokenstore}' for future use.\n"
        )
        try:
            # Ask for credentials if not set as environment variables
            if not email or not password:
                email, password = get_credentials()

            garmin = Garmin(email, password)
            garmin.login()
            # Save tokens for next login
            garmin.garth.dump(tokenstore)

        except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError, requests.exceptions.HTTPError) as err:
            logger.error(err)
            return None

    return garmin


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
