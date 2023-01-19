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

for i in range(10):
    # Init API
    if not api:
        api, last_activity = getc.get_last_activity()
    else:
        break


activity_id = last_activity["activityId"]
today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)
x = []
weight = []
filename_prefix ="2023_01_19"

for data in api.get_body_composition(startdate.isoformat(), today.isoformat())["dateWeightList"]:
    x.append(datetime.datetime.fromtimestamp(data['date'] / 1000))
    weight.append(data['weight'] / 1000)

fig, ax = plt.subplots(figsize=(15, 5.2))
ax.set_xlabel('Súly')
ax.set_ylabel('Dátum')
ax.plot(x, weight, label='Súly')
plt.legend()
plt.savefig(filename_prefix + '_weight.png')
plt.show()


