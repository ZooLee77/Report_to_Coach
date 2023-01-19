# from fitparse import FitFile
# from matplotlib.dates import AutoDateFormatter, AutoDateLocator
# from statistics import mean
# from scipy.signal import savgol_filter
# from IPython.display import display, HTML
# from typing import Any

from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
import datetime
from tabulate import tabulate
# import pandas as pd
import read_fit_file_func as readfit
import get_cloud_data as getc
import json


api = None
relative_effort = ''
text_weather = ''
today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)
x = []
weight = []

feel_map ={0: "Nagyon gyenge", 25: "Gyenge", 50: "Normál", 75: "Erős", 100: "Nagyon erős"}
rpe_map ={10: "1/10 - Nagyon könnyű", 20: "2/10 - Könnyű", 30: "3/10 - Mérsékelt", 40: "4/10 - Kissé nehéz",
          50: "5/10- Nehéz", 60: "6/10- Nehéz", 70: "7/10- Nagyon nehéz", 80: "8/10- Nagyon nehéz", 90: "9/10- Rendkívül nehéz"
          , 100: "Maximális"}

for i in range(10):
    # Init API
    if not api:
        api, last_activity = getc.get_last_activity()
    else:
        break

activity_id = last_activity["activityId"]
#print(json.dumps(last_activity, indent=4))
fit_file_name = getc.download_activity(api, activity_id)

evaluation = api.get_activity_evaluation(activity_id)
if "directWorkoutFeel" in evaluation['summaryDTO'].keys():
    feel = feel_map[evaluation['summaryDTO']['directWorkoutFeel']]
    rpe = rpe_map[evaluation['summaryDTO']['directWorkoutRpe']]
    relative_effort = "Hogy érzi magát? " + feel + " Észlelt erőfeszítés: " + rpe

weather = api.get_activity_weather(activity_id)
if isinstance(weather['temp'], (int, float)):
    text_weather = "Hömérséklet: " + "{0:.4}".format((weather['temp'] - 32) / 1.8) + "(C) Hőérzet: " + "{0:.4}".format(
        (150 - 32) / 1.8) + "(C) Páratartalom: " + str(
        weather['relativeHumidity']) + "% Szélsebesség: " + "{0:.4}".format(weather['windSpeed'] * 1.852) + " kmp"

for data in api.get_body_composition(startdate.isoformat(), today.isoformat())["dateWeightList"]:
    x.append(datetime.datetime.fromtimestamp(data['date'] / 1000))
    weight.append(data['weight'] / 1000)

# fit_file_list = ['10153960586_ACTIVITY.fit', '10168131101_ACTIVITY.fit', '10176445328_ACTIVITY.fit',
#                  '10190995780_ACTIVITY.fit', '10197069218_ACTIVITY.fit', '10207850540_ACTIVITY.fit',
#                  '10217521774_ACTIVITY.fit', '10225157717_ACTIVITY.fit', '10241888920_ACTIVITY.fit']

records_dataframe = readfit.read_fit_file_records(fit_file_name)
laps_dataframe = readfit.read_fit_file_laps(fit_file_name)
workout_dic = readfit.read_fit_file_workout(fit_file_name)

# for file in fit_file_list:
#     records_dataframe = readfit.read_fit_file_records(file)
#     laps_dataframe = readfit.read_fit_file_laps(file)
#     workout_dic = readfit.read_fit_file_workout(file)

# print(start_time)

filename_prefix = laps_dataframe["Kör kezdő idő"].iloc[0].strftime("%Y_%m_%d_%H_%M_%S")

laps_dataframe.insert(laps_dataframe.columns.get_loc("Max. pulzus") + 1, 'Min. pulzus', np.nan)
for e in range(len(laps_dataframe.index)):
    temp_start = laps_dataframe["Kör kezdő idő"].iloc[e]
    temp_end = laps_dataframe["Kör vége"].iloc[e]
    temp_min = records_dataframe.query(
        'Rec_Timestamp > @temp_start and Rec_Timestamp < @temp_end').Heartrate.min()
    laps_dataframe.loc[e + 1, ['Min. pulzus']] = temp_min
    filt = ((records_dataframe['Rec_Timestamp'] >= temp_start) & (records_dataframe['Rec_Timestamp'] < temp_end))
    if not np.isnan(laps_dataframe['Workout_index'][e + 1]):
        if 'Workout_intensity' not in laps_dataframe.keys():
            laps_dataframe['Workout_intensity'] = np.nan
        laps_dataframe.loc[e + 1, ['Workout_intensity']] = workout_dic['data']['Workout_intensity'][
            int(laps_dataframe['Workout_index'][e + 1])]
        if workout_dic['data']['Workout_target_type'][int(laps_dataframe['Workout_index'][e + 1])] == 'heart_rate':
            if 'Workout_HR_min' not in records_dataframe.keys():
                records_dataframe['Workout_HR_min'] = np.nan
                records_dataframe['Workout_HR_max'] = np.nan
            records_dataframe.loc[filt, 'Workout_HR_min'] = workout_dic['data']['Workout_target_low'][
                int(laps_dataframe['Workout_index'][e + 1])]
            records_dataframe.loc[filt, 'Workout_HR_max'] = workout_dic['data']['Workout_target_high'][
                int(laps_dataframe['Workout_index'][e + 1])]
        if workout_dic['data']['Workout_target_type'][int(laps_dataframe['Workout_index'][e + 1])] == 'speed':
            if 'Workout_speed_min' not in records_dataframe.keys():
                records_dataframe['Workout_speed_min'] = np.nan
                records_dataframe['Workout_speed_max'] = np.nan
            records_dataframe.loc[filt, 'Workout_speed_min'] = workout_dic['data']['Workout_target_low'][
                int(laps_dataframe['Workout_index'][e + 1])]
            records_dataframe.loc[filt, 'Workout_speed_max'] = workout_dic['data']['Workout_target_high'][
                int(laps_dataframe['Workout_index'][e + 1])]

laps_dataframe.loc[len(laps_dataframe.index), ["Átlagos pulzusszám"]] = records_dataframe["Heartrate"].mean()
if 'Workout_HR_min' in records_dataframe.keys():
    temp_filt = ((records_dataframe['Heartrate'] >= records_dataframe['Workout_HR_min']) & (
            records_dataframe['Heartrate'] <= records_dataframe['Workout_HR_max']))
    workout_dic['HR percent'] = records_dataframe.loc[temp_filt, 'Heartrate'].count() / sum(
        records_dataframe['Workout_HR_min'] > 0)
if 'Workout_speed_min' in records_dataframe.keys():
    temp_filt = ((records_dataframe['Speed'] >= records_dataframe['Workout_speed_min']) & (
            records_dataframe['Speed'] <= records_dataframe['Workout_speed_max']))
    workout_dic['Speed percent'] = records_dataframe.loc[temp_filt, 'Speed'].count() / sum(
        records_dataframe['Workout_speed_min'] > 0)


def format_timedelta(td):
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    else:
        return '{:02d}:{:02d}'.format(minutes, seconds)


laps_dataframe['Kör idő'] = laps_dataframe.apply(lambda x: format_timedelta(x["Kör idő"]), axis=1)
# for e in range(len(lap_total_elapsed_time)):
#     lap_total_elapsed_time[e]=format_timedelta(lap_total_elapsed_time[e])

laps_dataframe['Összesített idő'] = laps_dataframe.apply(lambda x: format_timedelta(x["Összesített idő"]), axis=1)
# for e in range(len(lap_sum_time)):
#     lap_sum_time[e]=format_timedelta(lap_sum_time[e])

laps_dataframe['Kör vége'] = laps_dataframe['Kör vége'].dt.strftime("%H:%M:%S")
# for e in range(len(lap_time_stamps)):
#     lap_time_stamps[e]=lap_time_stamps[e].strftime("%H:%M:%S")

laps_dataframe['Kör kezdő idő'] = laps_dataframe['Kör kezdő idő'].dt.strftime("%H:%M:%S")


# for e in range(len(lap_start_time)):
#     lap_start_time[e]=lap_start_time[e].strftime("%H:%M:%S")


def format_speed(speed):
    lap_minute, lap_second = divmod(1000 / (speed * 60), 1)
    return '{: 02d}:{: 02d}'.format(int(lap_minute), int(lap_second * 60))


if laps_dataframe['Sport'][1] == 'running':
    laps_dataframe['Átlagos tempó'] = laps_dataframe.apply(lambda x: format_speed(x["Átlagos tempó"]), axis=1)
    # for e in range(len(lap_average_speed)):
    #     lap_minute, lap_second = divmod(1000/(lap_average_speed[e]*60),1)
    #     lap_average_speed[e]='{:02d}:{:02d}'.format(int(lap_minute), int(lap_second*60))

    laps_dataframe['Max. tempó'] = laps_dataframe.apply(lambda x: format_speed(x["Max. tempó"]), axis=1)
    # for e in range(len(lap_max_speed)):
    #     lap_minute, lap_second = divmod(1000/(lap_max_speed[e]*60),1)
    #     lap_max_speed[e]='{:02d}:{:02d}'.format(int(lap_minute), int(lap_second*60))

#    for e in range(len(speed)):
#        lap_minute, lap_second = divmod(1000/max((speed[e]*60),3),1)
#        speed[e]='{:02d}:{:02d}'.format(int(lap_minute), int(lap_second*60))

if laps_dataframe['Sport'][1] == 'cycling':
    laps_dataframe['Átlagos sebesség'] = laps_dataframe['Átlagos sebesség'] * 3.6
    # for e in range(len(lap_average_speed)):
    #     lap_average_speed[e]=lap_average_speed[e]*3.6

    laps_dataframe['Max. sebesség'] = laps_dataframe['Max. sebesség'] * 3.6
    # for e in range(len(lap_max_speed)):
    #     lap_max_speed[e]=lap_max_speed[e]*3.6

    records_dataframe['Speed'] = records_dataframe['Speed'] * 3.6
    # for e in range(len(speed)):
    #     speed[e]=speed[e]*3.6

# for e in range(len(speed)):
#     lap_minute, lap_second = divmod(1000/(speed[e]*60),1)
#     speed[e]='{:02d}:{:02d}'.format(int(lap_minute), int(lap_second*60))


# display(df)
# print(tabulate(df, headers="keys", tablefmt="tsv"))

text = """
Hello, Friend.

Here is your data:
Workout name is {WorkoutName}
Workout Heart Rate in the target zone: {HRPercent}
Workout Speed in the target zone: {SpeedPercent}
{Relative_effort}
{Weather}

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
<p>Workout name is {WorkoutName}</p>
<p>Workout Heart Rate in the target zone: {HRPercent}</p>
<p>Workout Speed in the target zone: {SpeedPercent}</p>
<p>{Relative_effort}</p>
<p>{Weather}</p>

{table}
<p>Regards,</p>
<p>Me</p>
</body></html>
"""
text = text.format(table=tabulate(laps_dataframe, headers="keys", tablefmt="grid")
                   , WorkoutName=workout_dic['Workout_Name']
                   , HRPercent="{0:.2%}".format(workout_dic['HR percent'])
                   , SpeedPercent="{0:.2%}".format(workout_dic['Speed percent'])
                   , Relative_effort=relative_effort, Weather=text_weather)
html = html.format(table=tabulate(laps_dataframe, headers="keys", tablefmt="html")
                   , WorkoutName=workout_dic['Workout_Name']
                   , HRPercent="{0:.2%}".format(workout_dic['HR percent'])
                   , SpeedPercent="{0:.2%}".format(workout_dic['Speed percent'])
                   , Relative_effort=relative_effort, Weather=text_weather)

f = open(filename_prefix + '_data.html', 'w')
f.write(html)
f.close()

f = open(filename_prefix + '_data.txt', 'w')
f.write(text)
f.close()

fig, ax = plt.subplots(figsize=(15, 5.2))
ax.set_xlabel('Súly')
ax.set_ylabel('Dátum')
ax.plot(x, weight, label='Súly')
plt.legend()
plt.savefig(filename_prefix + '_weight.png')


def plotter_dict(first, second=None, third=None):
    x = []

    def time_ticks(s, pos):
        d = datetime.timedelta(seconds=s)
        return str(d)

    fig, ax1 = plt.subplots(figsize=(15, 5.2))
    ax1.set_xlabel('Seconds')
    xtick_formatter = ticker.FuncFormatter(time_ticks)
    ax1.xaxis.set_major_formatter(xtick_formatter)
    ax1.grid(True)
    for i in range(len(first['data'])):
        x.append(i)
    ax1.set_ylabel(first['label'])
    plt.xlim([0, len(first['data'])])
    lns1 = ax1.plot(x, first['data'], color=first['plot_color'], label=first['label'])
    filename_suffix = first['suffix']
    lns = lns1
    if second is not None:
        if second['suffix'].__contains__('WKT'):
            lns2 = ax1.plot(x, second['data'], color=second['plot_color'], label=second['label'])
        else:
            ax2 = ax1.twinx()
            ax2.set_ylabel(second['label'])
            lns2 = ax2.plot(x, second['data'], color=second['plot_color'], label=second['label'])
        lns += lns2
        filename_suffix += second['suffix']
    if third is not None:
        if third['suffix'].__contains__('WKT'):
            lns3 = ax1.plot(x, third['data'], color=third['plot_color'], label=third['label'])
        else:
            ax3 = ax1.twinx()
            ax3.spines.right.set_position(("axes", 1.06))
            ax3.set_ylabel(third['label'])
            lns3 = ax3.plot(x, third['data'], color=third['plot_color'], label=third['label'])
        lns += lns3
        filename_suffix += third['suffix']
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
    plt.tight_layout()
    plt.savefig(filename_prefix + filename_suffix + '.png')


breath_dict = {'label': 'Légzésszám', 'plot_color': '#B0E1F7', 'suffix': '_breath', 'data': records_dataframe['Breath']}
heart_rate_dict = {'label': 'Pulzusszám', 'plot_color': '#ff0035', 'suffix': '_HR',
                   'data': records_dataframe['Heartrate']}
speed_dict = {'label': 'Sebesség', 'plot_color': '#05C4EB', 'suffix': '_speed', 'data': records_dataframe['Speed']}
gear_ratio_dict = {'label': 'Gear Ratio', 'plot_color': '#F38D18', 'suffix': '_gear',
                   'data': records_dataframe['GearRatio']}
altitude_dict = {'label': 'Magasság', 'plot_color': '#57D25F', 'suffix': '_alt', 'data': records_dataframe['Altitude']}
if laps_dataframe['Sport'][1] == 'cycling':
    power_dict = {'label': 'Power átlag 3sec', 'plot_color': '#FF6AE6', 'suffix': '_power',
                  'data': records_dataframe['Power_smooth_3_FFT']}
    cadence_dict = {'label': 'Kerékütem', 'plot_color': '#FFB70E', 'suffix': '_cadence',
                    'data': records_dataframe['Cadence']}
else:  # if lap_sport[0] == 'running':
    power_dict = {'label': 'Power', 'plot_color': '#FF6AE6', 'suffix': '_power',
                  'data': records_dataframe['Power']}
    cadence_dict = {'label': 'Pedálütem', 'plot_color': '#FFB70E', 'suffix': '_cadence',
                    'data': records_dataframe['Cadence']}
if 'Workout_HR_min' in records_dataframe.keys():
    workout_heart_rate_min_dict = {'label': 'Pulzusszám cél min', 'plot_color': '#FF00E6', 'suffix': '_WKT_HR_min',
                                   'data': records_dataframe['Workout_HR_min']}
    workout_heart_rate_max_dict = {'label': 'Pulzusszám cél max', 'plot_color': '#DF04C9', 'suffix': '_WKT_HR_max',
                                   'data': records_dataframe['Workout_HR_max']}
    plotter_dict(heart_rate_dict, workout_heart_rate_min_dict, workout_heart_rate_max_dict)
if 'Workout_speed_min' in records_dataframe.keys():
    workout_speed_min_dict = {'label': 'Sebesség cél min', 'plot_color': '#0590EC', 'suffix': '_WKT_speed_min',
                              'data': records_dataframe['Workout_speed_min']}
    workout_speed_max_dict = {'label': 'Sebesség cél max', 'plot_color': '#0569EC', 'suffix': '_WKT_speed_max',
                              'data': records_dataframe['Workout_speed_max']}
    plotter_dict(speed_dict, workout_speed_min_dict, workout_speed_max_dict)

plotter_dict(speed_dict, heart_rate_dict)
if not np.isnan(breath_dict['data'].iloc[-1]):
    plotter_dict(breath_dict, heart_rate_dict, speed_dict)
    plotter_dict(power_dict, breath_dict, heart_rate_dict)
    plotter_dict(breath_dict, heart_rate_dict)
plotter_dict(cadence_dict, heart_rate_dict)
plotter_dict(heart_rate_dict)
if not np.isnan(altitude_dict['data'].iloc[-1]):
    if not np.isnan(gear_ratio_dict['data'].iloc[-1]):
        plotter_dict(cadence_dict, gear_ratio_dict, altitude_dict)
    plotter_dict(cadence_dict, speed_dict, altitude_dict)

# records_dataframe = pd.DataFrame()
# start_time = 0
# power = []
# #power_smooth_10 = []
# power_smooth_3_FFT = []
# #temp_smoth = []
# heart_rate = []
# cadence = []
# speed = []
# breath = []
# timestamp = []
# #i = 0
# altitude = []
# gear_ratio = []
# #temp_avarage = 0
# x = []

#
# lap_start_time = []
# lap_time_stamps = []
# lap_total_elapsed_time = []
# lap_distance = []
# lap_average_hr = []
# lap_max_hr = []
# lap_min_hr = []
# lap_average_speed = []
# lap_max_speed = []
# lap_ascent = []
# lap_descent = []
# lap_power = []
# lap_sum_time = []
# lap_sport = []
# lap_average_cadence = []
# lap_max_cadence = []
# lap_normalized_power = []


#
# def plotter (first, second=None, third=None):
#     x = []
#
#     def timeTicks(x, pos):
#         d = datetime.timedelta(seconds=x)
#         return str(d)
#
#     fig, ax1 = plt.subplots(figsize=(15, 5.2))
#     ax1.set_xlabel('Seconds')
#     xtick_formatter = mpl.ticker.FuncFormatter(timeTicks)
#     ax1.xaxis.set_major_formatter(xtick_formatter)
#     ax1.grid(True)
#     if first == breath:
#         for i in range(len(breath)):
#             x.append(i)
#         ax1.set_ylabel('Légzésszám')
#         plt.xlim([0, len(breath)])
#         lns1 = ax1.plot(x, breath, color='#B0E1F7', label='Légzésszám')
#         filename_suffix = '_breath'
#         lns = lns1
#     if first == speed:
#         for i in range(len(speed)):
#             x.append(i)
#         ax1.set_ylabel('Sebesség')
#         plt.xlim([0, len(speed)])
#         lns1 = ax1.plot(x, speed, color='#05C4EB', label='Sebesség')
#         filename_suffix = '_speed'
#         lns = lns1
#     if first == cadence:
#         for i in range(len(cadence)):
#             x.append(i)
#         ax1.set_ylabel('Kerékütem')
#         plt.xlim([0, len(cadence)])
#         lns1 = ax1.plot(x, cadence, color='#FFB70E', label='Kerékütem')
#         filename_suffix = '_cadence'
#         lns = lns1
#     if first == heart_rate:
#         for i in range(len(heart_rate)):
#             x.append(i)
#         ax1.set_ylabel('Pulzusszám')
#         plt.xlim([0, len(heart_rate)])
#         lns1 = ax1.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
#         filename_suffix = '_HR'
#         lns = lns1
#     if second == heart_rate:
#         ax2 = ax1.twinx()
#         ax2.set_ylabel('Pulzusszám')
#         lns2 = ax2.plot(x, heart_rate, color='#ff0035', label='Pulzusszám')
#         lns += lns2
#         filename_suffix += '_HR'
#     if third == speed:
#         ax3 = ax1.twinx()
#         ax3.spines.right.set_position(("axes", 1.06))
#         ax3.set_ylabel('Sebesség')
#         lns3 = ax3.plot(x, speed, color='#05C4EB', label='Sebesség')
#         lns += lns3
#         filename_suffix += '_speed'
#     if third == power:
#         ax3 = ax1.twinx()
#         ax3.spines.right.set_position(("axes", 1.06))
#         if lap_sport[0] == 'cycling':
#             ax3.set_ylabel('Power átlag 3sec')
#             lns3 = ax3.plot(x, power_smooth_3_FFT, color='#FF6AE6', label='Power átlag 3sec')
#         if lap_sport[0] == 'running':
#             ax3.set_ylabel('Power')
#             lns3 = ax3.plot(x, power, color='#FF6AE6', label='Power')
#         lns += lns3
#         filename_suffix += '_power'
#     labs = [l.get_label() for l in lns]
#     ax1.legend(lns, labs, loc=0)
#     plt.tight_layout()
#     plt.savefig(filename_prefix + filename_suffix + '.png')
# plotter (speed,heart_rate)
# plotter (breath,heart_rate,speed)
# plotter (breath,heart_rate,power)
# plotter (breath,heart_rate)
# plotter (cadence,heart_rate)
# plotter (heart_rate)


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
#
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
