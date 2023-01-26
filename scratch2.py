import numpy as np
from fitparse import FitFile
import matplotlib.pyplot as plt
import matplotlib.pyplot as pyplot
#import numpy as np
import pandas as pd
#import matplotlib as mpl
#from tabulate import tabulate
from scipy.signal import savgol_filter
import read_fit_file as readfit
import get_cloud_data as getc
import json
import datetime
from tabulate import tabulate
import myfitnesspal
import os

def format_timedelta(td):
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    else:
        return '{:02d}:{:02d}'.format(minutes, seconds)

api = None
# Load environment variables if defined
email = os.getenv("garmin_email")
password = os.getenv("garmin_password")

print(email)
print(password)

# for i in range(10):
#     # Init API
#     if not api:
#         api, last_activity = getc.get_last_activity()
#     else:
#         break


# activity_id = last_activity["activityId"]
today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)
filename_prefix ="2023_01_19"
sleep_text = ''
sleep_list = []
#
# client = myfitnesspal.Client()
# day = client.get_date(today)
#
# meal_name = [today, 'Név']
# meal_quantity = ['', 'Mennyiség']
# meal_calories = ['', 'Kalória']
# meal_sum_calories = 0
#
# for meals in day.meals:
#     meal_name.append(meals.name)
#     meal_quantity.append('')
#     meal_calories.append('')
#     for entries in meals.entries:
#         meal_name.append(entries.name)
#         meal_quantity.append(entries.quantity)
#         meal_calories.append(entries['calories'])
#         meal_sum_calories += float(entries['calories'])
#
# meal_name.append("Összesen")
# meal_quantity.append('')
# meal_calories.append(meal_sum_calories)
# meal_data_df = pd.DataFrame([meal_name, meal_quantity, meal_calories])
# print(meal_data_df.transpose())
#
# # "bodyBatteryChargedValue": 37,
# # "bodyBatteryDrainedValue": 0,
# # "bodyBatteryHighestValue": 81,
# # "bodyBatteryLowestValue": 44,
#
