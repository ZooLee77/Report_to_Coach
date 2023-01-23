import numpy as np
from fitparse import FitFile
import matplotlib.pyplot as plt
import matplotlib.pyplot as pyplot
#import numpy as np
import pandas as pd
#import matplotlib as mpl
#from tabulate import tabulate
from scipy.signal import savgol_filter
import read_fit_file_func as readfit
import get_cloud_data as getc
import json
import datetime


api = None

# for i in range(10):
#     # Init API
#     if not api:
#         api, last_activity = getc.get_last_activity()
#     else:
#         break
#

# activity_id = last_activity["activityId"]
today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)
filename_prefix ="2023_01_19"

# x = []
# activityszint = []
# sleep = api.get_sleep_data(today.isoformat())
# for data in sleep["sleepLevels"]:
#     x.append(datetime.datetime.fromisoformat(data['startGMT']))
#     x.append(datetime.datetime.fromisoformat(data['endGMT'])-datetime.timedelta(seconds=1))
#     activityszint.append(data['activityLevel'])
#     activityszint.append(data['activityLevel'])

x = np.array([datetime.datetime(2023, 1, 21, 22, 17), datetime.datetime(2023, 1, 21, 22, 20, 59), datetime.datetime(2023, 1, 21, 22, 21), datetime.datetime(2023, 1, 21, 22, 54, 59), datetime.datetime(2023, 1, 21, 22, 55), datetime.datetime(2023, 1, 21, 23, 29, 59), datetime.datetime(2023, 1, 21, 23, 30), datetime.datetime(2023, 1, 21, 23, 51, 59), datetime.datetime(2023, 1, 21, 23, 52), datetime.datetime(2023, 1, 22, 0, 27, 59), datetime.datetime(2023, 1, 22, 0, 28), datetime.datetime(2023, 1, 22, 0, 31, 59), datetime.datetime(2023, 1, 22, 0, 32), datetime.datetime(2023, 1, 22, 0, 41, 59), datetime.datetime(2023, 1, 22, 0, 42), datetime.datetime(2023, 1, 22, 0, 59, 59), datetime.datetime(2023, 1, 22, 1, 0), datetime.datetime(2023, 1, 22, 1, 22, 59), datetime.datetime(2023, 1, 22, 1, 23), datetime.datetime(2023, 1, 22, 1, 29, 59), datetime.datetime(2023, 1, 22, 1, 30), datetime.datetime(2023, 1, 22, 1, 38, 59), datetime.datetime(2023, 1, 22, 1, 39), datetime.datetime(2023, 1, 22, 1, 52, 59), datetime.datetime(2023, 1, 22, 1, 53), datetime.datetime(2023, 1, 22, 2, 13, 59), datetime.datetime(2023, 1, 22, 2, 14), datetime.datetime(2023, 1, 22, 2, 17, 59), datetime.datetime(2023, 1, 22, 2, 18), datetime.datetime(2023, 1, 22, 2, 48, 59), datetime.datetime(2023, 1, 22, 2, 49), datetime.datetime(2023, 1, 22, 3, 16, 59), datetime.datetime(2023, 1, 22, 3, 17), datetime.datetime(2023, 1, 22, 3, 56, 59), datetime.datetime(2023, 1, 22, 3, 57), datetime.datetime(2023, 1, 22, 4, 2, 59), datetime.datetime(2023, 1, 22, 4, 3), datetime.datetime(2023, 1, 22, 4, 19, 59), datetime.datetime(2023, 1, 22, 4, 20), datetime.datetime(2023, 1, 22, 5, 7, 59), datetime.datetime(2023, 1, 22, 5, 8), datetime.datetime(2023, 1, 22, 5, 13, 59), datetime.datetime(2023, 1, 22, 5, 14), datetime.datetime(2023, 1, 22, 5, 36, 59), datetime.datetime(2023, 1, 22, 5, 37), datetime.datetime(2023, 1, 22, 5, 38, 59), datetime.datetime(2023, 1, 22, 5, 39), datetime.datetime(2023, 1, 22, 6, 44, 59)])
activityszint = np.array([1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 3.0, 3.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 3.0, 3.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0])

#x = np.array([datetime.datetime(2023, 1, 21, 22, 17), datetime.datetime(2023, 1, 21, 22, 20, 59), datetime.datetime(2023, 1, 21, 22, 21), datetime.datetime(2023, 1, 21, 22, 54, 59)])
#activityszint = np.array([1.0, 1.0, 0.0, 0.0])

mely = np.array([-0.1] * len(activityszint)) #004C99
eber = np.array([0.9] * len(activityszint)) #66B2FF
rem = np.array([1.9] * len(activityszint)) #990099
ebrenlet = np.array([2.9] * len(activityszint)) #FF66B2

fig, ax = plt.subplots(figsize=(15, 5.2))
ax.set_ylabel('Alvási szakaszok')
ax.set_xlabel('Dátum')
plt.ylim([-1, max(activityszint)])
ax.plot(x, activityszint, label='Alvás')
ax.fill_between(x, -1, 0, where=((activityszint > mely).all(activityszint < eber)), color='#004C99', alpha=0.5)
ax.fill_between(x, -1, 1, where=((activityszint > eber) and (activityszint < rem)), color='#66B2FF', alpha=0.5)
ax.fill_between(x, -1, 2, where=((activityszint > rem) and (activityszint < ebrenlet)), color='#990099', alpha=0.5)
ax.fill_between(x, -1, 3, where=(activityszint > ebrenlet), color='#FF66B2', alpha=0.5)

#plt.savefig(filename_prefix + '_weight.png')
plt.show()
