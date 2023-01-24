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
from tabulate import tabulate

def format_timedelta(td):
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    else:
        return '{:02d}:{:02d}'.format(minutes, seconds)

api = None

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

