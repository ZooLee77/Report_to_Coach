from fitparse import FitFile
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateFormatter, AutoDateLocator
import numpy as np
from statistics import mean
from scipy.signal import savgol_filter
import datetime
from tabulate import tabulate
import pandas as pd
from IPython.display import display, HTML

fit_file = FitFile('10168131101_ACTIVITY.fit')


# for record in fit_file.get_messages("lap"):
#     # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
#     for data in record:
#         # Print the name and value of the data (and the units if it has any)
#         if data.units:
#             print(f"{data.name}, {data.value}, {data.units}")
#         else:
#             print(f"{data.name} {data.value}")
#

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
heart_rate = []
cadence = []
speed = []
breath = []
i = 0
temp_avarage = 0
x = []
filename_prefix = '2022_12_21_20_24'

for record in fit_file.get_messages("record"):
    # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
    for data in record:
        # Print the name and value of the data (and the units if it has any)
        if data.name == ('Power') or data.name == ('power'):
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
        if data.name == 'unknown_108': #breath
            breath.append(data.value/100)
        if data.name == 'timestamp':
            if start_time == 0 :
                start_time = data.value
            x.append(data.value-start_time)
        if data.name == 'enhanced_speed':
            speed.append(data.value)
        if data.name == 'heart_rate':
            heart_rate.append(data.value)
        if data.name == 'cadence':
            cadence.append(data.value)

    if len(breath) < len(x) :
        breath.append(20)

lap_start_time = []
lap_time_stamps = []
lap_total_elapsed_time = []
lap_distance = []
lap_average_hr = []
lap_max_hr = []
lap_average_speed = []
lap_max_speed = []
lap_ascent = []
lap_descent = []
lap_power = []

for lap in fit_file.get_messages("lap"):
    # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
    for data in lap:
        # Print the name and value of the data (and the units if it has any)
        if data.name == ('start_time') :
            lap_start_time.append(data.value)
        if data.name == 'timestamp':
            lap_time_stamps.append(data.value)
        if data.name == 'total_elapsed_time':
            lap_total_elapsed_time.append(data.value)
        if data.name == 'total_distance':
            lap_distance.append(data.value)
        if data.name == 'avg_heart_rate':
            lap_average_hr.append(data.value)
        if data.name == 'max_heart_rate':
            lap_max_hr.append(data.value)
        if data.name == 'enhanced_avg_speed':
            if isinstance(data.value, float) :
                lap_average_speed.append(data.value)
        if data.name == 'enhanced_max_speed':
            if isinstance(data.value, float) :
                lap_max_speed.append(data.value)
        if data.name == 'total_ascent':
            lap_ascent.append(data.value)
        if data.name == 'total_descent':
            lap_descent.append(data.value)
        if data.name == 'Lap Power':
            lap_power.append(data.value)



df = pd.DataFrame({"Kör kedző idő": lap_start_time, "Időpont": lap_time_stamps,
                "lap_total_elapsed_time": lap_total_elapsed_time, "lap_distance": lap_distance,
                "lap_average_hr": lap_average_hr, "lap_max_hr": lap_max_hr,
                "lap_average_speed": lap_average_speed, "lap_max_speed": lap_max_speed,
                "lap_ascent": lap_ascent, "lap_descent": lap_descent, "lap_power": lap_power})
df.index += 1


display(df)

f = open('table.txt', 'w')
f.write(tabulate(df, headers="keys", tablefmt="rounded_grid"))
f.close()

yhat = savgol_filter(power, 151, 3) # window size 51, polynomial order 3
print('power',len(power))
print('power_smoth',len(power_smoth))
print('yhat',len(yhat))
print('breath', len(breath))
print('x', len(x))
print('speed', len(speed))
print('heart_rate', len(heart_rate))
print('cadence', len(cadence))

x = []
for i in range(len(breath)):
  x.append(i)


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

def timeTicks(x, pos):
    d = datetime.timedelta(seconds=x)
    return str(d)

fig, ax1 = plt.subplots(figsize=(15, 5.2))
ax2 = ax1.twinx()

ax1.set_xlabel('Seconds')
ax1.set_ylabel('Sebesség')
ax2.set_ylabel('Pulzusszám')
plt.xlim([0, len(breath)])
xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
ax1.xaxis.set_major_formatter(xtick_formatter)
lns1 = ax1.plot(x, speed, color='#05C4EB', label='Sebesség')
lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
ax1.grid(True)

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

# plt.legend()
plt.tight_layout()
plt.savefig(filename_prefix + '_Speed_HR.png')
#plt.show()
#plt.close()
#print(start_time)

fig, ax1 = plt.subplots(figsize=(15, 5.2))

ax1.set_xlabel('Seconds')
ax1.set_ylabel('Légzésszám')
plt.xlim([0, len(breath)])
xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
ax1.xaxis.set_major_formatter(xtick_formatter)
lns1 = ax1.plot(x, breath, color='#B0E1F7', label='Légzésszám')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.set_ylabel('Pulzusszám')
lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')

ax3 = ax1.twinx()
ax3.spines.right.set_position(("axes", 1.06))
ax3.set_ylabel('Sebesség')
lns3 = ax3.plot(x, speed, color='#05C4EB', label='Sebesség')


lns = lns1+lns2+lns3
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

# plt.legend()
plt.tight_layout()
plt.savefig(filename_prefix + '_Breath_HR_Speed.png')
#plt.show()

fig, ax1 = plt.subplots(figsize=(15, 5.2))

ax1.set_xlabel('Seconds')
ax1.set_ylabel('Légzésszám')
plt.xlim([0, len(breath)])
xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
ax1.xaxis.set_major_formatter(xtick_formatter)
lns1 = ax1.plot(x, breath, color='#B0E1F7', label='Légzésszám')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.set_ylabel('Pulzusszám')
lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')

ax3 = ax1.twinx()
ax3.spines.right.set_position(("axes", 1.06))
ax3.set_ylabel('Power')
lns3 = ax3.plot(x, power_smoth, color='#FF6AE6', label='Power')


lns = lns1+lns2+lns3
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

# plt.legend()
plt.tight_layout()
plt.savefig(filename_prefix + '_Breath_HR_Power.png')
#plt.show()



fig, ax1 = plt.subplots(figsize=(15, 5.2))
ax2 = ax1.twinx()

ax1.set_xlabel('Seconds')
ax1.set_ylabel('Légzésszám')
ax2.set_ylabel('Pulzusszám')
plt.xlim([0, len(breath)])
xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
ax1.xaxis.set_major_formatter(xtick_formatter)
lns1 = ax1.plot(x, breath, color='#B0E1F7', label='Légzésszám')
lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
ax1.grid(True)

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

# plt.legend()
plt.tight_layout()
plt.savefig(filename_prefix + '_Breath_HR.png')
#plt.show()


fig, ax1 = plt.subplots(figsize=(15, 5.2))
ax2 = ax1.twinx()

ax1.set_xlabel('Seconds')
ax1.set_ylabel('Kerékütem')
ax2.set_ylabel('Pulzusszám')
plt.xlim([0, len(breath)])
xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
ax1.xaxis.set_major_formatter(xtick_formatter)
lns1 = ax1.plot(x, cadence, color='#FFB70E', label='Kerékütem')
lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
ax1.grid(True)

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)

# plt.legend()
plt.tight_layout()
plt.savefig(filename_prefix + '_Cadence_HR.png')
#plt.show()


#plt.plot(x, power, color='green')
fig, ax = plt.subplots(figsize=(15, 5.2))
ax.set_xlabel('Seconds')
ax.set_ylabel('Pulzusszám')
plt.xlim([0, len(heart_rate)])
xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
ax.xaxis.set_major_formatter(xtick_formatter)
ax.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
ax.grid(True)

plt.legend()
plt.tight_layout()
plt.savefig(filename_prefix + '_HR.png')
#plt.show()
#print(plt.style.available)
#xtick_locator = AutoDateLocator()
#xtick_formatter = AutoDateFormatter(xtick_locator)
#xtick_formatter.scaled[1/(24*60)] = my_format_function

#ax.xaxis.set_major_locator(xtick_locator)
#plt.plot(x, yhat, color='red')
#breat B0E1F7
#cadence FFB70E
#hear rate ff0035
#power FF6AE6
#speed 05C4EB
#plt.style.use('seaborn-pastel')
