import numpy as np
from fitparse import FitFile
import matplotlib.pyplot as plt
import matplotlib.pyplot as pyplot
#import numpy as np
from statistics import mean
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

for i in range(10):
    # Init API
    if not api:
        api, last_activity = getc.get_last_activity()
    else:
        break


# activity_id = last_activity["activityId"]
today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)
filename_prefix ="2023_01_19"
sleep_text = ''
sleep_list = []

x = []
rhr_list = []
filename_prefix = today.strftime("%Y_%m_%d")
startdate = today - datetime.timedelta(days=7)
while startdate <= today:
    rhr_date = api.get_rhr_day(startdate.isoformat())
    x.append(startdate)
    rhr_list.append(rhr_date['allMetrics']['metricsMap']['WELLNESS_RESTING_HEART_RATE'][0]['value'])
    startdate += datetime.timedelta(days=1)
meanRHR = np.array([mean(rhr_list)] * len(rhr_list))
fig, ax = plt.subplots(figsize=(15, 5.2))
ax.set_xlabel('Dátum')
ax.set_ylabel('Resting Heart Rate')
ax.plot(x, rhr_list, label='Resting Heart Rate')
ax.plot(x, meanRHR, label="Átlagos RHR")
ax.text((x[-1] - x[0]) / 2 + x[0], meanRHR[0] + (max(rhr_list)-min(rhr_list))/20, "{0:.3}".format(meanRHR[0]))
plt.legend()
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
