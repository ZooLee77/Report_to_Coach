import numpy as np
from fitparse import FitFile
#import matplotlib.pyplot as plt
#import matplotlib.pyplot as pyplot
#import numpy as np
import pandas as pd
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#from tabulate import tabulate
from scipy.signal import savgol_filter
import read_fit_file_func as readfit
import get_cloud_data as getc
import json
import datetime


api = None

for i in range(10):
    # Init API
    if not api:
        api, last_activity = getc.get_last_activity()
    else:
        break


activity_id = last_activity["activityId"]
activities = api.get_activities(1, 20)
for activity in activities:
    activity_id = activity["activityId"]
    getc.display_text(activity_id)
    evaluation = api.get_activity_evaluation(activity_id)
    if "directWorkoutFeel" in evaluation['summaryDTO'].keys():
        print(evaluation['summaryDTO']['directWorkoutFeel'])
        print(evaluation['summaryDTO']['directWorkoutRpe'])
    weather = api.get_activity_weather(activity_id)
    if isinstance(weather['temp'], (int, float)):
        print("temp", (weather['temp']-32)/1.8)
        print("apparent", (weather['apparentTemp']-32)/1.8)
        print("relativeHumidity", weather['relativeHumidity'])
        print("windSpeed", weather['windSpeed']*1.852)



