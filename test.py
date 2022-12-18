from fitparse import FitFile
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateFormatter, AutoDateLocator
import numpy as np
from statistics import mean
from scipy.signal import savgol_filter
import datetime

fit_file = FitFile('8234833773_ACTIVITY.fit')

def my_format_function(x, pos=None):
    x = mpl.dates.num2date(x)
    if pos == 0:
        fmt = '%D %H:%M:%S'
    else:
        fmt = '%H:%M:%S.%f'
    label = x.strftime(fmt)
    label = label.rstrip("0")
    label = label.rstrip(".")
    return label

# for record in fit_file.get_messages("record"):
#     # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
#     for data in record:
#         # Print the name and value of the data (and the units if it has any)
#         if data.units:
#             print(f"{data.name}, {data.value}, {data.units}")
#         else:
#             print(f"{data.name} {data.value}")


#for record in fit_file.get_messages("record"):
#     # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
#     for data in record:
#         # Print the name and value of the data (and the units if it has any)
#         if data.name == 'unknown_108':
#             print(f"{data.name}, {data.value}, {data.units}")

start_time = 0
power = []
power_smoth = []
temp_smoth = []
breath = []
i = 0
temp_avarage = 0
x = []
for record in fit_file.get_messages("record"):
    # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
    for data in record:
        # Print the name and value of the data (and the units if it has any)
        if data.name == 'power':
            i = i + 1
            power.append(data.value)
            temp_smoth.append(data.value)
            if i > 30:
                temp_avarage = mean(temp_smoth)
                del temp_smoth[0]
#               i = 0
#            else:
#                continue
            #atlagoljon 10 value-t es utana adja hozza
            power_smoth.append(temp_avarage)
        if data.name == 'unknown_108':
            breath.append(data.value/100)
        if data.name == 'timestamp':
            if start_time == 0 :
                start_time = data.value
            x.append(data.value-start_time)
    if len(breath) < len(x) :
        breath.append(20)


yhat = savgol_filter(power, 151, 3) # window size 51, polynomial order 3
print(len(power))
print(len(power_smoth))
print(len(breath))
print(len(x))

x = []
for i in range(len(breath)):
  x.append(i)

#plt.plot(x, power, color='green')
fig, ax = plt.subplots(figsize=(10, 5.2), layout='constrained')
ax.set_xlabel('Entry A')
ax.set_ylabel('Entry B')
#xtick_locator = AutoDateLocator()
#xtick_formatter = AutoDateFormatter(xtick_locator)
def timeTicks(x, pos):
    d = datetime.timedelta(seconds=x)
    return str(d)
xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
#xtick_formatter.scaled[1/(24*60)] = my_format_function

#ax.xaxis.set_major_locator(xtick_locator)
ax.xaxis.set_major_formatter(xtick_formatter)
#plt.plot(x, yhat, color='red')
ax.plot(x, breath)
ax.grid(True)

plt.show()