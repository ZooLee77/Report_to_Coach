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
#from IPython.display import display, HTML



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
#x = []

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
lap_sum_time = []
lap_sport = []

def read_fit_file(filename):
    global i, temp_avarage, start_time
    fit_file = FitFile(filename)

    # for record in fit_file.get_messages("lap"):
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
            # if data.name == 'timestamp':
            #     if start_time == 0 :
            #         start_time = data.value
            #     x.append(data.value-start_time)
            if data.name == 'enhanced_speed':
                speed.append(data.value)
            if data.name == 'heart_rate':
                heart_rate.append(data.value)
            if data.name == 'cadence':
                cadence.append(data.value)

        if len(breath) < len(heart_rate) :
            if len(breath) < 1:
                breath.append(20)
            else:
                breath.append(breath[-1])
        if len(speed) < len(heart_rate) :
            if len(speed) < 1:
                speed.append(0)
            else:
                speed.append(speed[-1])


    for lap in fit_file.get_messages("lap"):
        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in lap:
            # Print the name and value of the data (and the units if it has any)
            if data.name == ('start_time') :
                if start_time == 0 :
                    start_time = data.value
                lap_start_time.append(data.value)
            if data.name == 'timestamp':
                lap_time_stamps.append(data.value)
            if data.name == 'total_elapsed_time':
                lap_total_elapsed_time.append(datetime.timedelta(seconds=data.value))
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
            if data.name == 'Lap Power' or data.name == 'avg_power':
                if isinstance(data.value, int):
                    lap_power.append(data.value)
            if data.name == 'sport':
                lap_sport.append(data.value)

    for e in lap_time_stamps:
        lap_sum_time.append(e-lap_start_time[0])
    #print(lap_power)
    lap_start_time.append(min(lap_start_time))
    lap_time_stamps.append(max(lap_time_stamps))
    lap_total_elapsed_time.append(max(lap_time_stamps)-min(lap_start_time))
    lap_sum_time.append(max(lap_time_stamps)-min(lap_start_time))
    lap_average_speed.append(sum(lap_distance)/(max(lap_time_stamps)-min(lap_start_time)).total_seconds())
    lap_distance.append(sum(lap_distance))
    lap_average_hr.append(sum(heart_rate)/len(heart_rate))
    lap_max_hr.append(max(lap_max_hr))
    lap_max_speed.append(max(lap_max_speed))
    if isinstance(lap_ascent[0],int):
        lap_ascent.append(sum(lap_ascent))
    if isinstance(lap_descent[0],int):
        lap_descent.append(sum(lap_descent))
    lap_power.append(sum(lap_power)/len(lap_power))


read_fit_file('10197069218_ACTIVITY.fit')
#print(start_time)
filename_prefix = lap_start_time[0].strftime("%Y_%m_%d_%H_%M_%S")

def format_timedelta(td):
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    else:
        return '{:02d}:{:02d}'.format(minutes, seconds)

for e in range(len(lap_total_elapsed_time)):
    lap_total_elapsed_time[e]=format_timedelta(lap_total_elapsed_time[e])

for e in range(len(lap_sum_time)):
    lap_sum_time[e]=format_timedelta(lap_sum_time[e])

for e in range(len(lap_time_stamps)):
    lap_time_stamps[e]=lap_time_stamps[e].strftime("%H:%M:%S")

for e in range(len(lap_start_time)):
    lap_start_time[e]=lap_start_time[e].strftime("%H:%M:%S")

if lap_sport[0] == 'running':
    for e in range(len(lap_average_speed)):
        lap_minute, lap_second = divmod(1000/(lap_average_speed[e]*60),1)
        lap_average_speed[e]='{:02d}:{:02d}'.format(int(lap_minute), int(lap_second*60))

    for e in range(len(lap_max_speed)):
        lap_minute, lap_second = divmod(1000/(lap_max_speed[e]*60),1)
        lap_max_speed[e]='{:02d}:{:02d}'.format(int(lap_minute), int(lap_second*60))

    for e in range(len(speed)):
        lap_minute, lap_second = divmod(1000/max((speed[e]*60),3),1)
#        speed[e]='{:02d}:{:02d}'.format(int(lap_minute), int(lap_second*60))

if lap_sport[0] == 'cycling':
    for e in range(len(lap_average_speed)):
        lap_average_speed[e]=lap_average_speed[e]*3.6

    for e in range(len(lap_max_speed)):
        lap_max_speed[e]=lap_max_speed[e]*3.6

    for e in range(len(speed)):
        speed[e]=speed[e]*3.6

# for e in range(len(speed)):
#     lap_minute, lap_second = divmod(1000/(speed[e]*60),1)
#     speed[e]='{:02d}:{:02d}'.format(int(lap_minute), int(lap_second*60))

yhat = savgol_filter(power, 151, 3) # window size 51, polynomial order 3
print('power',len(power))
print('power_smoth',len(power_smoth))
print('yhat',len(yhat))
print('breath', len(breath))
#print('x', len(x))
print('speed', len(speed))
print('heart_rate', len(heart_rate))
print('cadence', len(cadence))

print('lap_start_time', len(lap_start_time))
print('lap_time_stamps', len(lap_time_stamps))
print('lap_power', len(lap_power))

df = pd.DataFrame({"Kör kezdő idő": lap_start_time, "Kör vége": lap_time_stamps,
                "Kör idő": lap_total_elapsed_time, "Összesített idő": lap_sum_time, "Távolság": lap_distance,
                "Átlagos pulzusszám": lap_average_hr, "Max. pulzus": lap_max_hr})

if lap_sport[0] == 'running':
    df['Átlagos tempó'] = lap_average_speed
    df['Max. tempó'] = lap_max_speed
if lap_sport[0] == 'cycling':
    df['Átlagos sebesség'] = lap_average_speed
    df['Max. sebesség'] = lap_max_speed
if (isinstance(lap_descent[0], int)):
    df['Teljes emelkedés'] = lap_ascent
    df['Teljes süllyedés'] = lap_descent
df['Teljesítmény'] = lap_power

df.index += 1

#display(df)
#print(tabulate(df, headers="keys", tablefmt="tsv"))

text = """
Hello, Friend.

Here is your data:

{table}

Regards,

Me"""

html = """
<html>
<head>
<style> 
  table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
  th, td {{ padding: 5px; }}
</style>
</head>
<body><p>Hello, Friend.</p>
<p>Here is your data:</p>
{table}
<p>Regards,</p>
<p>Me</p>
</body></html>
"""
text = text.format(table=tabulate(df, headers="keys", tablefmt="grid"))
html = html.format(table=tabulate(df, headers="keys", tablefmt="html"))

f = open(filename_prefix+'_data.html', 'w')
f.write(html)
f.close()

f = open(filename_prefix+'_data.txt', 'w')
f.write(text)
f.close()


def plotter (first, second=None, third=None):
    x = []

    def timeTicks(x, pos):
        d = datetime.timedelta(seconds=x)
        return str(d)

    fig, ax1 = plt.subplots(figsize=(15, 5.2))
    ax1.set_xlabel('Seconds')
    xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
    ax1.xaxis.set_major_formatter(xtick_formatter)
    ax1.grid(True)
    if first == breath:
        for i in range(len(breath)):
            x.append(i)
        ax1.set_ylabel('Légzésszám')
        plt.xlim([0, len(breath)])
        lns1 = ax1.plot(x, breath, color='#B0E1F7', label='Légzésszám')
        filename_suffix = '_breath'
        lns = lns1
    if first == speed:
        for i in range(len(speed)):
            x.append(i)
        ax1.set_ylabel('Sebesség')
        plt.xlim([0, len(speed)])
        lns1 = ax1.plot(x, speed, color='#05C4EB', label='Sebesség')
        filename_suffix = '_speed'
        lns = lns1
    if first == cadence:
        for i in range(len(cadence)):
            x.append(i)
        ax1.set_ylabel('Kerékütem')
        plt.xlim([0, len(cadence)])
        lns1 = ax1.plot(x, cadence, color='#FFB70E', label='Kerékütem')
        filename_suffix = '_cadence'
        lns = lns1
    if first == heart_rate:
        for i in range(len(heart_rate)):
            x.append(i)
        ax1.set_ylabel('Pulzusszám')
        plt.xlim([0, len(heart_rate)])
        lns1 = ax1.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
        filename_suffix = '_HR'
        lns = lns1
    if second == heart_rate:
        ax2 = ax1.twinx()
        ax2.set_ylabel('Pulzusszám')
        lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
        lns += lns2
        filename_suffix += '_HR'
    if third == speed:
        ax3 = ax1.twinx()
        ax3.spines.right.set_position(("axes", 1.06))
        ax3.set_ylabel('Sebesség')
        lns3 = ax3.plot(x, speed, color='#05C4EB', label='Sebesség')
        lns += lns3
        filename_suffix += '_speed'
    if third == power:
        ax3 = ax1.twinx()
        ax3.spines.right.set_position(("axes", 1.06))
        ax3.set_ylabel('Power')
        lns3 = ax3.plot(x, power, color='#FF6AE6', label='Power')
        lns += lns3
        filename_suffix += '_power'
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
    plt.tight_layout()
    plt.savefig(filename_prefix + filename_suffix + '.png')


plotter (speed,heart_rate)
plotter (breath,heart_rate,speed)
plotter (breath,heart_rate,power)
plotter (breath,heart_rate)
plotter (cadence,heart_rate)
plotter (heart_rate)

# def my_format_function(x, pos=None):
#     x = mpl.dates.num2date(x)
#     if pos == 0:
#         fmt = '%D %H:%M:%S'
#     else:
#         fmt = '%H:%M:%S.%f'
#     label = x.strftime(fmt)
#     label = label.rstrip("0")
#     label = label.rstrip(".")
#     return label

# x = []
# for i in range(len(breath)):
#   x.append(i)

# fig, ax1 = plt.subplots(figsize=(15, 5.2))
# ax2 = ax1.twinx()
#
# ax1.set_xlabel('Seconds')
# ax1.set_ylabel('Sebesség')
# ax2.set_ylabel('Pulzusszám')
# plt.xlim([0, len(breath)])
# xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
# ax1.xaxis.set_major_formatter(xtick_formatter)
# lns1 = ax1.plot(x, speed, color='#05C4EB', label='Sebesség')
# lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
# ax1.grid(True)
#
# lns = lns1+lns2
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=0)
#
# # plt.legend()
# plt.tight_layout()
# plt.savefig(filename_prefix + '_Speed_HR.png')
# #plt.show()
# #plt.close()
# #print(start_time)
#
# fig, ax1 = plt.subplots(figsize=(15, 5.2))
#
# ax1.set_xlabel('Seconds')
# ax1.set_ylabel('Légzésszám')
# plt.xlim([0, len(breath)])
# xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
# ax1.xaxis.set_major_formatter(xtick_formatter)
# lns1 = ax1.plot(x, breath, color='#B0E1F7', label='Légzésszám')
# ax1.grid(True)
#
# ax2 = ax1.twinx()
# ax2.set_ylabel('Pulzusszám')
# lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
#
# ax3 = ax1.twinx()
# ax3.spines.right.set_position(("axes", 1.06))
# ax3.set_ylabel('Sebesség')
# lns3 = ax3.plot(x, speed, color='#05C4EB', label='Sebesség')
#
#
# lns = lns1+lns2+lns3
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=0)
#
# # plt.legend()
# plt.tight_layout()
# plt.savefig(filename_prefix + '_Breath_HR_Speed.png')
# #plt.show()
#
# fig, ax1 = plt.subplots(figsize=(15, 5.2))
#
# ax1.set_xlabel('Seconds')
# ax1.set_ylabel('Légzésszám')
# plt.xlim([0, len(breath)])
# xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
# ax1.xaxis.set_major_formatter(xtick_formatter)
# lns1 = ax1.plot(x, breath, color='#B0E1F7', label='Légzésszám')
# ax1.grid(True)
#
# ax2 = ax1.twinx()
# ax2.set_ylabel('Pulzusszám')
# lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
#
# ax3 = ax1.twinx()
# ax3.spines.right.set_position(("axes", 1.06))
# ax3.set_ylabel('Power')
# #if cycle
# #lns3 = ax3.plot(x, power_smoth, color='#FF6AE6', label='Power')
# #if running
# lns3 = ax3.plot(x, power, color='#FF6AE6', label='Power')
#
# lns = lns1+lns2+lns3
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=0)
#
# # plt.legend()
# plt.tight_layout()
# plt.savefig(filename_prefix + '_Breath_HR_Power.png')
# #plt.show()
#
#
#
# fig, ax1 = plt.subplots(figsize=(15, 5.2))
# ax2 = ax1.twinx()
#
# ax1.set_xlabel('Seconds')
# ax1.set_ylabel('Légzésszám')
# ax2.set_ylabel('Pulzusszám')
# plt.xlim([0, len(breath)])
# xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
# ax1.xaxis.set_major_formatter(xtick_formatter)
# lns1 = ax1.plot(x, breath, color='#B0E1F7', label='Légzésszám')
# lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
# ax1.grid(True)
#
# lns = lns1+lns2
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=0)
#
# # plt.legend()
# plt.tight_layout()
# plt.savefig(filename_prefix + '_Breath_HR.png')
# #plt.show()
#
#
# fig, ax1 = plt.subplots(figsize=(15, 5.2))
# ax2 = ax1.twinx()
#
# ax1.set_xlabel('Seconds')
# ax1.set_ylabel('Kerékütem')
# ax2.set_ylabel('Pulzusszám')
# plt.xlim([0, len(breath)])
# xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
# ax1.xaxis.set_major_formatter(xtick_formatter)
# lns1 = ax1.plot(x, cadence, color='#FFB70E', label='Kerékütem')
# lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
# ax1.grid(True)
#
# lns = lns1+lns2
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=0)
#
# # plt.legend()
# plt.tight_layout()
# plt.savefig(filename_prefix + '_Cadence_HR.png')
# #plt.show()
#
#
# #plt.plot(x, power, color='green')
# fig, ax = plt.subplots(figsize=(15, 5.2))
# ax.set_xlabel('Seconds')
# ax.set_ylabel('Pulzusszám')
# plt.xlim([0, len(heart_rate)])
# xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
# ax.xaxis.set_major_formatter(xtick_formatter)
# ax.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
# ax.grid(True)
#
# plt.legend()
# plt.tight_layout()
# plt.savefig(filename_prefix + '_HR.png')
# #plt.show()
# #print(plt.style.available)
# #xtick_locator = AutoDateLocator()
# #xtick_formatter = AutoDateFormatter(xtick_locator)
# #xtick_formatter.scaled[1/(24*60)] = my_format_function
#
# #ax.xaxis.set_major_locator(xtick_locator)
# #plt.plot(x, yhat, color='red')
# #breat B0E1F7
# #cadence FFB70E
# #hear rate ff0035
# #power FF6AE6
# #speed 05C4EB
# #plt.style.use('seaborn-pastel')
