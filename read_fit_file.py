#import matplotlib as mpl
#import matplotlib.pyplot as plt
#from matplotlib.dates import AutoDateFormatter, AutoDateLocator
#from statistics import mean
#from IPython.display import display, HTML
#from tabulate import tabulate
from scipy.signal import savgol_filter
import datetime
import pandas as pd
from fitparse import FitFile
import numpy as np

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
        if len(breath) < len(timestamp):
            breath.append(np.nan)
        if len(speed) < len(timestamp):
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

    records_df = pd.DataFrame({"Rec_Timestamp": timestamp, "Heartrate": heart_rate,
                        "Altitude": altitude, "Speed": speed, "Cadence": cadence, "Breath": breath,
                        "GearRatio": gear_ratio, "Power": power, "Power_smooth_3_FFT": power_smooth_3_fft})


    return records_df

def read_fit_file_laps(filename):
    fit_file = FitFile(filename)
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
    lap_average_cadence = []
    lap_max_cadence = []
    lap_normalized_power = []
    lap_workout_step_index = []

    # for record in fit_file.get_messages("lap"):
    #     # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc.)
    #     for data in record:
    #         # Print the name and value of the data (and the units if it has any)
    #         if data.units:
    #             print(f"{data.name}, {data.value}, {data.units}")
    #         else:
    #             print(f"{data.name} {data.value}")
    for lap in fit_file.get_messages("lap"):
        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in lap:
            # Print the name and value of the data (and the units if it has any)
            if data.name == 'start_time':
                #                if start_time == 0 :
                #                    start_time = data.value
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
                if isinstance(data.value, float):
                    lap_average_speed.append(data.value)
            if data.name == 'enhanced_max_speed':
                if isinstance(data.value, float):
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
            if data.name == 'avg_cadence' or data.name == 'avg_running_cadence':
                lap_average_cadence.append(data.value)
            if data.name == 'max_cadence' or data.name == 'max_running_cadence':
                lap_max_cadence.append(data.value)
            if data.name == 'normalized_power':
                lap_normalized_power.append(data.value)
            if data.name == 'wkt_step_index':
                lap_workout_step_index.append(data.value)
    for i in lap_time_stamps:
        lap_sum_time.append(i - lap_start_time[0])
    lap_start_time.append(min(lap_start_time))
    lap_time_stamps.append(max(lap_time_stamps))
    lap_total_elapsed_time.append(max(lap_time_stamps) - min(lap_start_time))
    lap_sum_time.append(max(lap_time_stamps) - min(lap_start_time))
    lap_average_speed.append(sum(lap_distance) / (max(lap_time_stamps) - min(lap_start_time)).total_seconds())
    lap_distance.append(sum(lap_distance))
    lap_average_hr.append(sum(lap_average_hr) / len(lap_average_hr))
    lap_max_hr.append(max(lap_max_hr))
    if len(lap_max_speed) > 0:
        lap_max_speed.append(max(lap_max_speed))
    if isinstance(lap_ascent[0], int):
        lap_ascent.append(sum(lap_ascent))
    if isinstance(lap_descent[0], int):
        lap_descent.append(sum(lap_descent))
    lap_sport.append(lap_sport[-1])
    if len(lap_power) > 0:
        lap_power.append(sum(lap_power) / len(lap_power))
    # ellenorizni!
    if isinstance(lap_average_cadence[0], int):
        lap_average_cadence.append(sum(lap_average_cadence) / len(lap_average_cadence))
    lap_max_cadence.append(max(lap_max_cadence))
    if isinstance(lap_normalized_power[0], int):
        lap_normalized_power.append(sum(lap_normalized_power) / len(lap_normalized_power))
    lap_workout_step_index.append(np.nan)

    print('lap_start_time', len(lap_start_time))
    print('lap_time_stamps', len(lap_time_stamps))
    print('lap_power', len(lap_power))

    # workout_dic = read_fit_file_workout(fit_file_name)
    # print(workout_dic)
    # for file in fit_file_list:
    # workout_dic = read_fit_file_workout(file)
    # print(workout_dic)
    laps_df = pd.DataFrame({"Kör kezdő idő": lap_start_time, "Kör vége": lap_time_stamps,
                            "Kör idő": lap_total_elapsed_time, "Összesített idő": lap_sum_time,
                            "Távolság": lap_distance,
                            "Átlagos pulzusszám": lap_average_hr, "Max. pulzus": lap_max_hr})

    if lap_sport[0] == 'running':
        laps_df['Átlagos tempó'] = lap_average_speed
        laps_df['Max. tempó'] = lap_max_speed
    if lap_sport[0] == 'cycling':
        laps_df['Átlagos sebesség'] = lap_average_speed
        laps_df['Max. sebesség'] = lap_max_speed
    if isinstance(lap_average_cadence[0], int):
        laps_df['Átlagos kerékütem'] = lap_average_cadence
        laps_df['Max. kerékütem'] = lap_max_cadence
    if isinstance(lap_descent[0], int):
        laps_df['Teljes emelkedés'] = lap_ascent
        laps_df['Teljes süllyedés'] = lap_descent
    if len(lap_power) > 0:
        laps_df['Teljesítmény'] = lap_power
    if isinstance(lap_normalized_power[0], int):
        laps_df['Normalized Teljesítmény'] = lap_normalized_power
    laps_df['Sport'] = lap_sport
    laps_df['Workout_index'] = lap_workout_step_index
    laps_df.index += 1
    return laps_df

def read_fit_file_workout(filename):
#    global start_time, power_smooth_3_FFT
    #records_dataframe = pd.DataFrame()
    workout_step_duration = []
    workout_step_target_low = []
    workout_step_target_high = []
    workout_step_message_index = []
    workout_step_duration_type = []
    workout_step_target_type = []
    workout_step_target_value = []
    workout_step_intensity = []
    workout_name = ''
    workout_sport = ''
    fit_file = FitFile(filename)
    #workout_df = pd.DataFrame()

    for workout in fit_file.get_messages("workout"):
        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in workout:
            if data.name == 'wkt_name':
                workout_name = data.value
            if data.name == 'sport':
                workout_sport = data.value
    for workout_step in fit_file.get_messages("workout_step"):
        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        for data in workout_step:
#            print(data.name, data.value)
            if data.name == 'duration_time' or data.name == 'duration_distance' or data.name == 'duration_step':
                workout_step_duration.append(data.value)
            if data.name == 'custom_target_heart_rate_low' or data.name == 'custom_target_speed_low':
                workout_step_target_low.append(data.value)
            if data.name == 'custom_target_heart_rate_high' or data.name == 'custom_target_speed_high':
                workout_step_target_high.append(data.value)
            if data.name == 'message_index':
                workout_step_message_index.append(data.value)
            if data.name == 'duration_type':
                workout_step_duration_type.append(data.value)
            if data.name == 'target_value' or data.name == 'repeat_steps' or data.name == 'target_speed_zone'\
                    or data.name == 'target_hr_zone':
                workout_step_target_value.append(data.value)
            if data.name == 'target_type':
                workout_step_target_type.append(data.value)
            if data.name == 'intensity':
                workout_step_intensity.append(data.value)
        if len(workout_step_duration) < len(workout_step_message_index):
            workout_step_duration.append(np.nan)
        if len(workout_step_target_low) < len(workout_step_message_index):
            workout_step_target_low.append(np.nan)
        if len(workout_step_target_high) < len(workout_step_message_index):
            workout_step_target_high.append(np.nan)
        if len(workout_step_duration_type) < len(workout_step_message_index):
            workout_step_duration_type.append(np.nan)
        if len(workout_step_target_type) < len(workout_step_message_index):
            workout_step_target_type.append(np.nan)
        if len(workout_step_target_value) < len(workout_step_message_index):
            workout_step_target_value.append(np.nan)
        if len(workout_step_intensity) < len(workout_step_message_index):
            workout_step_intensity.append(np.nan)
    for i in range(len(workout_step_message_index)):
        if workout_step_message_index[i] != i:
            print("Error")
    workout_df = pd.DataFrame({'Workout_Duration': workout_step_duration
                        ,'Workout_duration_type': workout_step_duration_type, 'Workout_target_type': workout_step_target_type
                        ,'Workout_target_value': workout_step_target_value, 'Workout_intensity': workout_step_intensity, 'Workout_target_low': workout_step_target_low
                        ,'Workout_target_high': workout_step_target_high})
#    print(workout_name)
#    print(tabulate(workout_df, headers="keys", tablefmt="tsv"))
    return {'Workout_Name': workout_name, 'Workout_sport': workout_sport, 'HR percent': 0.0, 'Speed percent': 0.0, 'data': workout_df}
