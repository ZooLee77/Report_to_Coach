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



x = []
activityszint = []
filename_prefix = today.strftime("%Y_%m_%d")
sleep = api.get_sleep_data(today.isoformat())
for data in sleep["sleepLevels"]:
    x.append(datetime.datetime.strptime(data['startGMT'], "%Y-%m-%dT%H:%M:%S.%f"))
    x.append(datetime.datetime.strptime(data['endGMT'], "%Y-%m-%dT%H:%M:%S.%f") - datetime.timedelta(seconds=1))
    activityszint.append(data['activityLevel'])
    activityszint.append(data['activityLevel'])
eber = np.array([0.9] * len(activityszint))  # 66B2FF
rem = np.array([1.9] * len(activityszint))  # 990099
ebrenlet = np.array([2.9] * len(activityszint))  # FF66B2

fig, ax = plt.subplots(figsize=(15, 5.2))
ax.set_ylabel('Alvási szakaszok')
ax.set_xlabel('Dátum')
plt.ylim([-1, max(activityszint)])
ax.plot(x, activityszint, label='Alvás')
ax.fill_between(x, -1, 0, where=(activityszint < eber), color='#004C99', alpha=0.5)
ax.fill_between(x, -1, 1, where=(
    list(map(lambda x, y: x and y, (activityszint > eber), (activityszint < rem)))), color='#66B2FF', alpha=0.5)
ax.fill_between(x, -1, 2, where=(
    list(map(lambda x, y: x and y, (activityszint > rem), (activityszint < ebrenlet)))), color='#990099', alpha=0.5)
ax.fill_between(x, -1, 3, where=(activityszint > ebrenlet), color='#FF66B2', alpha=0.5)
plt.xlim(x[0], x[-1])
start_value = x[0].strftime("%m-%d %H:%M")
end_value = x[-1].strftime("%m-%d %H:%M")
ax.annotate(f"Start: {start_value}", xy=(ax.get_xlim()[0], -1), xycoords='data', xytext=(-50, -30),
            textcoords='offset points', arrowprops=dict(arrowstyle="->",
                                                        connectionstyle="arc3,rad=.2"))
ax.annotate(f"End: {end_value}", xy=(ax.get_xlim()[1], -1), xycoords='data', xytext=(-50, -30),
            textcoords='offset points', arrowprops=dict(arrowstyle="->",
                                                        connectionstyle="arc3,rad=.2"))
ax.set_yticks([0, 1, 2, 3])
plt.yticks(ticks=[0, 1, 2, 3], labels=["Mély", "Éber", "REM", "Ébrenlét"], fontsize=12)
plt.savefig(filename_prefix + '_sleep.png')
plt.close(fig)
sleep_data = [["Alvási adatok: ", "Alvási eredmény ", "Az alvás egésze ", "Alvásról visszajelzés ", "Teljes hossz ",
               "Alvási stress ", "Mély alvás ", "Könnyű alvás ", "REM ", "Ébrenlét "],
              [sleep['dailySleepDTO']['calendarDate'],
               str(sleep['dailySleepDTO']['sleepScores']["overall"]['value']) + " /100", '', '',
               format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['sleepTimeSeconds'])),
               sleep['dailySleepDTO']['avgSleepStress'],
               format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['deepSleepSeconds'])),
               format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['lightSleepSeconds'])),
               format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['remSleepSeconds'])),
               format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['awakeSleepSeconds']))],
              ['', '', sleep['dailySleepDTO']['sleepScores']["overall"]['qualifierKey'],
               sleep['dailySleepDTO']['sleepScoreFeedback'],
               sleep['dailySleepDTO']['sleepScores']["totalDuration"]['qualifierKey'],
               sleep['dailySleepDTO']['sleepScores']["stress"]['qualifierKey'],
               sleep['dailySleepDTO']['sleepScores']["deepPercentage"]['qualifierKey'],
               sleep['dailySleepDTO']['sleepScores']["lightPercentage"]['qualifierKey'],
               sleep['dailySleepDTO']['sleepScores']["remPercentage"]['qualifierKey'],
               sleep['dailySleepDTO']['sleepScores']["awakeCount"]['qualifierKey']]]
sleep_data_df = pd.DataFrame(sleep_data)
