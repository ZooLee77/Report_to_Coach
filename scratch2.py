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

def format_timedelta(td):
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    else:
        return '{:02d}:{:02d}'.format(minutes, seconds)

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

# x = np.array([datetime.datetime(2023, 1, 21, 22, 17), datetime.datetime(2023, 1, 21, 22, 20, 59), datetime.datetime(2023, 1, 21, 22, 21), datetime.datetime(2023, 1, 21, 22, 54, 59), datetime.datetime(2023, 1, 21, 22, 55), datetime.datetime(2023, 1, 21, 23, 29, 59), datetime.datetime(2023, 1, 21, 23, 30), datetime.datetime(2023, 1, 21, 23, 51, 59), datetime.datetime(2023, 1, 21, 23, 52), datetime.datetime(2023, 1, 22, 0, 27, 59), datetime.datetime(2023, 1, 22, 0, 28), datetime.datetime(2023, 1, 22, 0, 31, 59), datetime.datetime(2023, 1, 22, 0, 32), datetime.datetime(2023, 1, 22, 0, 41, 59), datetime.datetime(2023, 1, 22, 0, 42), datetime.datetime(2023, 1, 22, 0, 59, 59), datetime.datetime(2023, 1, 22, 1, 0), datetime.datetime(2023, 1, 22, 1, 22, 59), datetime.datetime(2023, 1, 22, 1, 23), datetime.datetime(2023, 1, 22, 1, 29, 59), datetime.datetime(2023, 1, 22, 1, 30), datetime.datetime(2023, 1, 22, 1, 38, 59), datetime.datetime(2023, 1, 22, 1, 39), datetime.datetime(2023, 1, 22, 1, 52, 59), datetime.datetime(2023, 1, 22, 1, 53), datetime.datetime(2023, 1, 22, 2, 13, 59), datetime.datetime(2023, 1, 22, 2, 14), datetime.datetime(2023, 1, 22, 2, 17, 59), datetime.datetime(2023, 1, 22, 2, 18), datetime.datetime(2023, 1, 22, 2, 48, 59), datetime.datetime(2023, 1, 22, 2, 49), datetime.datetime(2023, 1, 22, 3, 16, 59), datetime.datetime(2023, 1, 22, 3, 17), datetime.datetime(2023, 1, 22, 3, 56, 59), datetime.datetime(2023, 1, 22, 3, 57), datetime.datetime(2023, 1, 22, 4, 2, 59), datetime.datetime(2023, 1, 22, 4, 3), datetime.datetime(2023, 1, 22, 4, 19, 59), datetime.datetime(2023, 1, 22, 4, 20), datetime.datetime(2023, 1, 22, 5, 7, 59), datetime.datetime(2023, 1, 22, 5, 8), datetime.datetime(2023, 1, 22, 5, 13, 59), datetime.datetime(2023, 1, 22, 5, 14), datetime.datetime(2023, 1, 22, 5, 36, 59), datetime.datetime(2023, 1, 22, 5, 37), datetime.datetime(2023, 1, 22, 5, 38, 59), datetime.datetime(2023, 1, 22, 5, 39), datetime.datetime(2023, 1, 22, 6, 44, 59)])
# activityszint = np.array([1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 3.0, 3.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 3.0, 3.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0])
#
#
# mely = np.array([-0.1] * len(activityszint)) #004C99
# eber = np.array([0.9] * len(activityszint)) #66B2FF
# rem = np.array([1.9] * len(activityszint)) #990099
# ebrenlet = np.array([2.9] * len(activityszint)) #FF66B2
#
# fig, ax = plt.subplots(figsize=(15, 5.2))
# ax.set_ylabel('Alvási szakaszok')
# ax.set_xlabel('Dátum')
# plt.ylim([-1, max(activityszint)])
# ax.plot(x, activityszint, label='Alvás')
# ax.fill_between(x, -1, 0, where=(activityszint < eber), color='#004C99', alpha=0.5)
# ax.fill_between(x, -1, 1, where=(
#     list(map(lambda x, y: x and y, (activityszint > eber), (activityszint < rem)))), color='#66B2FF', alpha=0.5)
# ax.fill_between(x, -1, 2, where=(
#     list(map(lambda x, y: x and y, (activityszint > rem), (activityszint < ebrenlet)))), color='#990099', alpha=0.5)
# ax.fill_between(x, -1, 3, where=(activityszint > ebrenlet), color='#FF66B2', alpha=0.5)
# plt.xlim(x[0],x[-1])
# start_value = x[0].strftime("%m-%d %H:%M")
# end_value  = x[-1].strftime("%m-%d %H:%M")
# ax.annotate(f"Start: {start_value}", xy=(ax.get_xlim()[0], -1), xycoords='data', xytext=(-50, -30),
#             textcoords='offset points', arrowprops=dict(arrowstyle="->",
#             connectionstyle="arc3,rad=.2"))
# ax.annotate(f"End: {end_value}", xy=(ax.get_xlim()[1], -1), xycoords='data', xytext=(-50, -30),
#             textcoords='offset points', arrowprops=dict(arrowstyle="->",
#             connectionstyle="arc3,rad=.2"))
# ax.set_yticks([0, 1, 2, 3])
# plt.yticks(ticks=[0, 1, 2, 3], labels=["Mély", "Éber", "REM", "Ébrenlét"], fontsize=12)
# #plt.savefig(filename_prefix + '_weight.png')
# plt.show()

sleep = {'dailySleepDTO': {'id': 1674428520000, 'userProfilePK': 75371045, 'calendarDate': '2023-01-23', 'sleepTimeSeconds': 26578, 'napTimeSeconds': 0, 'sleepWindowConfirmed': True, 'sleepWindowConfirmationType': 'enhanced_confirmed_final', 'sleepStartTimestampGMT': 1674428520000, 'sleepEndTimestampGMT': 1674456538000, 'sleepStartTimestampLocal': 1674432120000, 'sleepEndTimestampLocal': 1674460138000, 'autoSleepStartTimestampGMT': None, 'autoSleepEndTimestampGMT': None, 'sleepQualityTypePK': None, 'sleepResultTypePK': None, 'unmeasurableSleepSeconds': 0, 'deepSleepSeconds': 5580, 'lightSleepSeconds': 13200, 'remSleepSeconds': 7740, 'awakeSleepSeconds': 1440, 'deviceRemCapable': True, 'retro': False, 'sleepFromDevice': True, 'averageSpO2Value': 90.0, 'lowestSpO2Value': 80, 'highestSpO2Value': 100, 'averageSpO2HRSleep': 51.0, 'averageRespirationValue': 14.0, 'lowestRespirationValue': 11.0, 'highestRespirationValue': 19.0, 'awakeCount': 1, 'avgSleepStress': 13.0, 'ageGroup': 'ADULT', 'sleepScoreFeedback': 'POSITIVE_LONG_AND_CALM', 'sleepScoreInsight': 'NONE', 'sleepScores': {'totalDuration': {'qualifierKey': 'GOOD', 'optimalStart': 28800.0, 'optimalEnd': 28800.0}, 'stress': {'qualifierKey': 'GOOD', 'optimalStart': 0.0, 'optimalEnd': 15.0}, 'awakeCount': {'qualifierKey': 'GOOD', 'optimalStart': 0.0, 'optimalEnd': 1.0}, 'overall': {'value': 89, 'qualifierKey': 'GOOD'}, 'remPercentage': {'qualifierKey': 'EXCELLENT', 'optimalStart': 21.0, 'optimalEnd': 31.0, 'idealStartInSeconds': 5581.38, 'idealEndInSeconds': 8239.18}, 'restlessness': {'qualifierKey': 'GOOD', 'optimalStart': 0.0, 'optimalEnd': 5.0}, 'lightPercentage': {'qualifierKey': 'EXCELLENT', 'optimalStart': 30.0, 'optimalEnd': 64.0, 'idealStartInSeconds': 7973.4, 'idealEndInSeconds': 17009.92}, 'deepPercentage': {'qualifierKey': 'EXCELLENT', 'optimalStart': 16.0, 'optimalEnd': 33.0, 'idealStartInSeconds': 4252.48, 'idealEndInSeconds': 8770.74}}, 'sleepVersion': 2}}
sleep_text = ""
sleep_text += "Alvási adatok: " + str(sleep['dailySleepDTO']['calendarDate']) + "\n"
sleep_text += "Alvási eredmény " + str(sleep['dailySleepDTO']['sleepScores']["overall"]['value']) + " /100\n"
sleep_text += "Az alvás egésze " + sleep['dailySleepDTO']['sleepScores']["overall"]['qualifierKey'] + "\n"
sleep_text += "Alvásról visszajelzés " + sleep['dailySleepDTO']['sleepScoreFeedback'] + "\n"
sleep_text += "Teljes hossz " + format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['sleepTimeSeconds']))
sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["totalDuration"]['qualifierKey'] + "\n"
sleep_text += "Alvási stress " + str(sleep['dailySleepDTO']['avgSleepStress'])
sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["stress"]['qualifierKey'] + "\n"
sleep_text += "Mély alvás " + format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['deepSleepSeconds']))
sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["deepPercentage"]['qualifierKey'] + "\n"
sleep_text += "Könnyű alvás " + format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['lightSleepSeconds']))
sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["lightPercentage"]['qualifierKey'] + "\n"
sleep_text += "REM " + format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['remSleepSeconds']))
sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["remPercentage"]['qualifierKey'] + "\n"
sleep_text += "Ébrenlét " + format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['awakeSleepSeconds']))
sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["awakeCount"]['qualifierKey'] + "\n"
sleep_text += "(**********************) " + "\n"
print(sleep_text)