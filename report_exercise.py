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
#import json

api = None
relative_effort = ''
text_weather = ''
sleep_text = ''
today = datetime.date.today()
#startdate = today - datetime.timedelta(days=7)
x = []
weight = []

feel_map = {0: "Nagyon gyenge", 25: "Gyenge", 50: "Normál", 75: "Erős", 100: "Nagyon erős"}
rpe_map = {10: "1/10 - Nagyon könnyű", 20: "2/10 - Könnyű", 30: "3/10 - Mérsékelt", 40: "4/10 - Kissé nehéz",
           50: "5/10- Nehéz", 60: "6/10- Nehéz", 70: "7/10- Nagyon nehéz", 80: "8/10- Nagyon nehéz",
           90: "9/10- Rendkívül nehéz",
           100: "Maximális"}

for i in range(10):
    # Init API
    if not api:
        api, last_activity = getc.get_last_activity()
    else:
        break

activity_id = last_activity["activityId"]
# activity_id = "10341956145"
# print(json.dumps(last_activity, indent=4))
fit_file_name = getc.download_activity(api, activity_id)


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


evaluation = api.get_activity_evaluation(activity_id)
if "directWorkoutFeel" in evaluation['summaryDTO'].keys():
    feel = feel_map[evaluation['summaryDTO']['directWorkoutFeel']]
    rpe = rpe_map[evaluation['summaryDTO']['directWorkoutRpe']]
    relative_effort = "Hogy érzi magát? " + feel + " Észlelt erőfeszítés: " + rpe

weather = api.get_activity_weather(activity_id)
if isinstance(weather['temp'], (int, float)):
    text_weather = "Hömérséklet: " + "{0:.4}".format((weather['temp'] - 32) / 1.8) + "(C) Hőérzet: " + "{0:.4}".format(
        (weather['apparentTemp'] - 32) / 1.8) + "(C) Páratartalom: " + str(
        weather['relativeHumidity']) + "% Szélsebesség: " + "{0:.4}".format(weather['windSpeed'] * 1.852) + " kmph"


def save_weight(api, actualday):
    x = []
    filename_prefix = actualday.strftime("%Y_%m_%d")
    startdate = actualday - datetime.timedelta(days=7)
    for data in api.get_body_composition(startdate.isoformat(), actualday.isoformat())["dateWeightList"]:
        x.append(datetime.datetime.fromtimestamp(data['date'] / 1000))
        weight.append(data['weight'] / 1000)
    fig, ax = plt.subplots(figsize=(15, 5.2))
    ax.set_xlabel('Súly')
    ax.set_ylabel('Dátum')
    ax.plot(x, weight, label='Súly')
    plt.legend()
    plt.savefig(filename_prefix + '_weight.png')


def save_sleep(api, date):
    def format_timedelta(td):
        minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        else:
            return '{:02d}:{:02d}'.format(minutes, seconds)

    x = []
    activityszint = []
    filename_prefix = date.strftime("%Y_%m_%d")
    sleep = api.get_sleep_data(date.isoformat())
    if not sleep['dailySleepDTO']['id']:
        return ""
    for data in sleep["sleepLevels"]:
        x.append(datetime.datetime.fromisoformat(data['startGMT']))
        x.append(datetime.datetime.fromisoformat(data['endGMT']) - datetime.timedelta(seconds=1))
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
    sleep_text = ""
    sleep_text += "Alvási adatok: " + str(sleep['dailySleepDTO']['calendarDate']) + "\n"
    sleep_text += "Alvási eredmény " + str(sleep['dailySleepDTO']['sleepScores']["overall"]['value']) + " /100\n"
    sleep_text += "Az alvás egésze " + sleep['dailySleepDTO']['sleepScores']["overall"]['qualifierKey'] + "\n"
    sleep_text += "Alvásról visszajelzés " + sleep['dailySleepDTO']['sleepScoreFeedback'] + "\n"
    sleep_text += "Teljes hossz " + format_timedelta(
        datetime.timedelta(seconds=sleep['dailySleepDTO']['sleepTimeSeconds']))
    sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["totalDuration"]['qualifierKey'] + "\n"
    sleep_text += "Alvási stress " + str(sleep['dailySleepDTO']['avgSleepStress'])
    sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["stress"]['qualifierKey'] + "\n"
    sleep_text += "Mély alvás " + format_timedelta(
        datetime.timedelta(seconds=sleep['dailySleepDTO']['deepSleepSeconds']))
    sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["deepPercentage"]['qualifierKey'] + "\n"
    sleep_text += "Könnyű alvás " + format_timedelta(
        datetime.timedelta(seconds=sleep['dailySleepDTO']['lightSleepSeconds']))
    sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["lightPercentage"]['qualifierKey'] + "\n"
    sleep_text += "REM " + format_timedelta(datetime.timedelta(seconds=sleep['dailySleepDTO']['remSleepSeconds']))
    sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["remPercentage"]['qualifierKey'] + "\n"
    sleep_text += "Ébrenlét " + format_timedelta(
        datetime.timedelta(seconds=sleep['dailySleepDTO']['awakeSleepSeconds']))
    sleep_text += " " + sleep['dailySleepDTO']['sleepScores']["awakeCount"]['qualifierKey'] + "\n"
    sleep_text += "(**********************) " + "\n"
    return sleep_text


save_weight(api, today)

current_date = datetime.datetime.fromisoformat(last_activity['startTimeGMT']).date()
while current_date <= today:
    sleep_text += save_sleep(api, current_date)
    current_date += datetime.timedelta(days=1)

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
{sleep}
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
<p>{sleep}</p>
<p>Regards,</p>
<p>Me</p>
</body></html>
"""
text = text.format(table=tabulate(laps_dataframe, headers="keys", tablefmt="grid"),
                   WorkoutName=workout_dic['Workout_Name'],
                   HRPercent="{0:.2%}".format(workout_dic['HR percent']),
                   SpeedPercent="{0:.2%}".format(workout_dic['Speed percent']),
                   Relative_effort=relative_effort, Weather=text_weather, sleep=sleep_text)
html = html.format(table=tabulate(laps_dataframe, headers="keys", tablefmt="html"),
                   WorkoutName=workout_dic['Workout_Name'],
                   HRPercent="{0:.2%}".format(workout_dic['HR percent']),
                   SpeedPercent="{0:.2%}".format(workout_dic['Speed percent']),
                   Relative_effort=relative_effort, Weather=text_weather, sleep=sleep_text)

f = open(filename_prefix + '_data.html', 'w')
f.write(html)
f.close()

f = open(filename_prefix + '_data.txt', 'w')
f.write(text)
f.close()


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
