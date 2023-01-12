import numpy as np
from fitparse import FitFile
#import matplotlib.pyplot as plt
#import matplotlib.pyplot as pyplot
#import numpy as np
import pandas as pd
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#from tabulate import tabulate

df = pd.DataFrame({"Timesta":[10,20,30,40,50,60,70,80,90],"Heartrate":[10,11,12,13,14,15,16,17,18]})
sales_data = pd.DataFrame({"name":["William","Emma","Sofia","Markus","Edward","Thomas","Ethan","Olivia","Arun","Anika","Paulo"]
,"region":["East","North","East","South","West","West","South","West","West","East","South"]
,"sales":[50000,52000,90000,34000,42000,72000,49000,55000,67000,65000,67000]
,"expenses":[42000,43000,50000,44000,38000,39000,42000,60000,39000,44000,45000]})
Altitude = [42000,43000,50000,44000,38000,39000,42000,60000,39000,44000,45000]
Altitude2 = [4200,4300,5000,4400,3800,3900,4200,6000,3900,4400,4500]

Altitude_dict = {'Label': 'Magassag', 'plot_color': '#FF6AE6', 'suffix': '_alt', 'data':Altitude}
Altitude_dict2 = {'Label': 'Magassag2', 'plot_color': '#05C4EB', 'suffix': '_alt2', 'data':Altitude2}
#print(isinstance(Altitude_dict['data'][-1],int))
#print(df['Timestamp'],type)
#print(sales_data.query('sales > 60000'))
#filt=(df['Timesta'] > 3 & df['Timesta'] < 60)
#below = df.query('Timesta < 60')
#print(df.query('Timesta < 60 and Timesta > 11').Heartrate.min())
fit_file_list = []
fit_file_list.append('10153960586_ACTIVITY.fit') #3
fit_file_list.append('10168131101_ACTIVITY.fit') #2
fit_file_list.append('10176445328_ACTIVITY.fit') #3
fit_file_list.append('10190995780_ACTIVITY.fit') #1
fit_file_list.append('10197069218_ACTIVITY.fit') #2
fit_file_list.append('10207850540_ACTIVITY.fit') #5
fit_file_list.append('10217521774_ACTIVITY.fit') #2
fit_file_list.append('10225157717_ACTIVITY.fit') #1
fit_file_list.append('10241888920_ACTIVITY.fit') #7

fit_file_name = '10241888920_ACTIVITY.fit' #7

def read_fit_file_records(filename):
    power = []
    #power_smooth_3_fft = []
    heart_rate = []
    cadence = []
    speed = []
    breath = []
    timestamp = []
    altitude = []
    gear_ratio = []

    #records_dataframe = pd.DataFrame()
    fit_file = FitFile(filename)

    #for record in fit_file.get_messages("record"):
    #     # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc.)
    #     for data in record:
    #         # Print the name and value of the data (and the units if it has any)
    #         if data.name == 'unknown_108':
    #             print(f"{data.name}, {data.value}, {data.units}")

    for record in fit_file.get_messages("record"):
        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in record:
            # Print the name and value of the data (and the units if it has any)
            if data.name == 'Power' or data.name == 'power':
                power.append(data.value)
            if data.name == 'unknown_108': #breath
                breath.append(data.value/100)
            if data.name == 'timestamp':
                timestamp.append(data.value)
            if data.name == 'enhanced_speed':
                speed.append(data.value)
            if data.name == 'heart_rate':
                heart_rate.append(data.value)
            if data.name == 'cadence':
                cadence.append(data.value)
            if data.name == 'enhanced_altitude':
                altitude.append(data.value)
            if data.name == 'currGearRatio':
                gear_ratio.append(data.value)
        if len(breath) < len(timestamp) :
            breath.append(np.nan)
        if len(speed) < len(timestamp) :
            speed.append(np.nan)
        if len(power) < len(timestamp):
            power.append(np.nan)
        if len(cadence) < len(timestamp):
            cadence.append(np.nan)
        if len(altitude) < len(timestamp):
            altitude.append(np.nan)
        if len(gear_ratio) < len(timestamp):
            gear_ratio.append(np.nan)

    # power_smooth_10_FFT = savgol_filter(power, 151, 3) # window size 151, polynomial order 3
    #negativot kiszedni!
    power_smooth_3_fft = savgol_filter(power, 51, 3)  # window size 51, polynomial order 3
    print('Rec_Timestamp', len(timestamp))
    print('heart_rate', len(heart_rate))
    print('power', len(power))
    # print('power_smooth_10', len(power_smooth_10))
    print('power_smooth_3_fft', len(power_smooth_3_fft))
    print('breath', len(breath))
    # print('x', len(x))
    print('speed', len(speed))
    print('cadence', len(cadence))

    records_df = pd.DataFrame({"Rec_Timestamp":timestamp,"Heartrate":heart_rate,
                        "Altitude":altitude,"Speed":speed,"Cadence":cadence,"Breath":breath,
                        "GearRatio":gear_ratio,"Power":power,"Power_smooth_3_FFT":power_smooth_3_fft})


    return records_df

workout_dic = read_fit_file_workout(fit_file_name)
print(workout_dic)
for file in fit_file_list:
    workout_dic = read_fit_file_workout(file)
    print(workout_dic)
