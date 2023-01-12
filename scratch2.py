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
import datetime

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

fit_file_name = '10292432582_ACTIVITY.fit' #7

fit_file = FitFile(fit_file_name)
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
        if data.name == 'start_time' :
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
        if data.name == 'avg_cadence' or data.name == 'avg_running_cadence':
            lap_average_cadence.append(data.value)
        if data.name == 'max_cadence' or data.name == 'max_running_cadence':
            lap_max_cadence.append(data.value)
        if data.name == 'normalized_power':
            lap_normalized_power.append(data.value)
        if data.name == 'wkt_step_index':
            lap_workout_step_index.append(data.value)
for i in lap_time_stamps:
    lap_sum_time.append(i-lap_start_time[0])
lap_start_time.append(min(lap_start_time))
lap_time_stamps.append(max(lap_time_stamps))
lap_total_elapsed_time.append(max(lap_time_stamps)-min(lap_start_time))
lap_sum_time.append(max(lap_time_stamps)-min(lap_start_time))
lap_average_speed.append(sum(lap_distance)/(max(lap_time_stamps)-min(lap_start_time)).total_seconds())
lap_distance.append(sum(lap_distance))
lap_average_hr.append(sum(lap_average_hr) / len(lap_average_hr))
lap_max_hr.append(max(lap_max_hr))
if len(lap_max_speed) > 0:
    lap_max_speed.append(max(lap_max_speed))
if isinstance(lap_ascent[0],int):
    lap_ascent.append(sum(lap_ascent))
if isinstance(lap_descent[0],int):
    lap_descent.append(sum(lap_descent))
lap_sport.append(lap_sport[-1])
if len(lap_power) > 0:
    lap_power.append(sum(lap_power)/len(lap_power))
# ellenorizni!
if isinstance(lap_average_cadence[0],int):
    lap_average_cadence.append(sum(lap_average_cadence)/len(lap_average_cadence))
lap_max_cadence.append(max(lap_max_cadence))
if isinstance(lap_normalized_power[0],int):
    lap_normalized_power.append(sum(lap_normalized_power)/len(lap_normalized_power))
lap_workout_step_index.append(np.nan)

print('lap_start_time', len(lap_start_time))
print('lap_time_stamps', len(lap_time_stamps))
print('lap_power', len(lap_power))

#workout_dic = read_fit_file_workout(fit_file_name)
#print(workout_dic)
#for file in fit_file_list:
    #workout_dic = read_fit_file_workout(file)
    #print(workout_dic)
laps_df = pd.DataFrame({"Kör kezdő idő": lap_start_time, "Kör vége": lap_time_stamps,
                        "Kör idő": lap_total_elapsed_time, "Összesített idő": lap_sum_time, "Távolság": lap_distance,
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

# {'activityId': 10292432582, 'activityName': 'Kardió', 'description': None, 'startTimeLocal': '2023-01-12 07:08:10',
# 'startTimeGMT': '2023-01-12 06:08:10', 'activityType': {'typeId': 11, 'typeKey': 'indoor_cardio', 'parentTypeId':
# 29, 'isHidden': False, 'sortOrder': None, 'restricted': False, 'trimmable': True}, 'eventType': {'typeId': 9,
# 'typeKey': 'uncategorized', 'sortOrder': 10}, 'comments': None, 'parentId': None, 'distance': 0.0, 'duration':
# 3880.47607421875, 'elapsedDuration': 3880.47607421875, 'movingDuration': 0.0, 'elevationGain': None,
# 'elevationLoss': None, 'averageSpeed': 0.0, 'maxSpeed': None, 'startLatitude': None, 'startLongitude': None,
# 'hasPolyline': False, 'ownerId': 75371045, 'ownerDisplayName': '67df95a9-0c48-47a3-965c-5e75732b9385',
# 'ownerFullName': 'Fejes Zoltán', 'ownerProfileImageUrlSmall':
# 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/581284d0-e41d-4d12-8914-6b0c667574ce-75371045.png',
# 'ownerProfileImageUrlMedium': 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/603fc184-dc8a-4f12-978a
# -2ed1406ada6e-75371045.png', 'ownerProfileImageUrlLarge':
# 'https://s3.amazonaws.com/garmin-connect-prod/profile_images/37349b34-59b1-435d-9652-67056684468d-75371045.png',
# 'calories': 658.0, 'averageHR': 126.0, 'maxHR': 168.0, 'averageRunningCadenceInStepsPerMinute': None,
# 'maxRunningCadenceInStepsPerMinute': None, 'averageBikingCadenceInRevPerMinute': None,
# 'maxBikingCadenceInRevPerMinute': None, 'averageSwimCadenceInStrokesPerMinute': None,
# 'maxSwimCadenceInStrokesPerMinute': None, 'averageSwolf': None, 'activeLengths': None, 'steps': None,
# 'conversationUuid': None, 'conversationPk': None, 'numberOfActivityLikes': None, 'numberOfActivityComments': None,
# 'likedByUser': None, 'commentedByUser': None, 'activityLikeDisplayNames': None, 'activityLikeFullNames': None,
# 'activityLikeProfileImageUrls': None, 'requestorRelationship': None, 'userRoles': ['ROLE_OUTDOOR_USER',
# 'ROLE_CONNECTUSER', 'ROLE_FITNESS_USER', 'ROLE_MARINE_USER', 'ROLE_WELLNESS_USER', 'ROLE_TACX_APP_USER'],
# 'privacy': {'typeId': 3, 'typeKey': 'subscribers'}, 'userPro': False, 'courseId': None, 'poolLength': None,
# 'unitOfPoolLength': None, 'hasVideo': False, 'videoUrl': None, 'timeZoneId': 124, 'beginTimestamp': 1673503690000,
# 'sportTypeId': 4, 'avgPower': None, 'maxPower': None, 'aerobicTrainingEffect': 2.799999952316284,
# 'anaerobicTrainingEffect': 2.0, 'strokes': None, 'normPower': None, 'leftBalance': None, 'rightBalance': None,
# 'avgLeftBalance': None, 'max20MinPower': None, 'avgVerticalOscillation': None, 'avgGroundContactTime': None,
# 'avgStrideLength': None, 'avgFractionalCadence': None, 'maxFractionalCadence': None, 'trainingStressScore': None,
# 'intensityFactor': None, 'vO2MaxValue': None, 'avgVerticalRatio': None, 'avgGroundContactBalance': None,
# 'lactateThresholdBpm': None, 'lactateThresholdSpeed': None, 'maxFtp': None, 'avgStrokeDistance': None,
# 'avgStrokeCadence': None, 'maxStrokeCadence': None, 'workoutId': None, 'avgStrokes': None, 'minStrokes': None,
# 'deviceId': 3322744951, 'minTemperature': 20.0, 'maxTemperature': None, 'minElevation': None, 'maxElevation': None,
# 'avgDoubleCadence': None, 'maxDoubleCadence': None, 'summarizedExerciseSets': None, 'maxDepth': None, 'avgDepth':
# None, 'surfaceInterval': None, 'startN2': None, 'endN2': None, 'startCns': None, 'endCns': None,
# 'summarizedDiveInfo': {'weight': None, 'weightUnit': None, 'visibility': None, 'visibilityUnit': None,
# 'surfaceCondition': None, 'current': None, 'waterType': None, 'waterDensity': None, 'summarizedDiveGases': [],
# 'totalSurfaceTime': None}, 'activityLikeAuthors': None, 'avgVerticalSpeed': None, 'maxVerticalSpeed': None,
# 'floorsClimbed': None, 'floorsDescended': None, 'manufacturer': 'GARMIN', 'diveNumber': None, 'locationName': None,
# 'bottomTime': None, 'lapCount': 1, 'endLatitude': None, 'endLongitude': None, 'minAirSpeed': None, 'maxAirSpeed':
# None, 'avgAirSpeed': None, 'avgWindYawAngle': None, 'minCda': None, 'maxCda': None, 'avgCda': None,
# 'avgWattsPerCda': None, 'flow': None, 'grit': None, 'jumpCount': None, 'caloriesEstimated': None,
# 'caloriesConsumed': None, 'waterEstimated': 596.0, 'waterConsumed': None, 'maxAvgPower_1': None, 'maxAvgPower_2':
# None, 'maxAvgPower_5': None, 'maxAvgPower_10': None, 'maxAvgPower_20': None, 'maxAvgPower_30': None,
# 'maxAvgPower_60': None, 'maxAvgPower_120': None, 'maxAvgPower_300': None, 'maxAvgPower_600': None,
# 'maxAvgPower_1200': None, 'maxAvgPower_1800': None, 'maxAvgPower_3600': None, 'maxAvgPower_7200': None,
# 'maxAvgPower_18000': None, 'excludeFromPowerCurveReports': None, 'totalSets': None, 'activeSets': None,
# 'totalReps': None, 'minRespirationRate': 15.34000015258789, 'maxRespirationRate': 39.900001525878906,
# 'avgRespirationRate': 27.68000030517578, 'trainingEffectLabel': 'AEROBIC_BASE', 'activityTrainingLoad':
# 85.75869750976562, 'avgFlow': None, 'avgGrit': None, 'minActivityLapDuration': 3880.47607421875, 'avgStress': None,
# 'startStress': None, 'endStress': None, 'differenceStress': None, 'maxStress': None,
# 'aerobicTrainingEffectMessage': 'MAINTAINING_AEROBIC_BASE_7', 'anaerobicTrainingEffectMessage':
# 'MAINTAINING_ANAEROBIC_BASE_1', 'splitSummaries': [], 'hasSplits': False, 'moderateIntensityMinutes': 27,
# 'vigorousIntensityMinutes': 31, 'maxBottomTime': None, 'hasSeedFirstbeatProfile': None, 'calendarEventId': None,
# 'calendarEventUuid': None, 'avgGradeAdjustedSpeed': None, 'avgWheelchairCadence': None, 'maxWheelchairCadence':
# None, 'pr': False, 'purposeful': False, 'manualActivity': False, 'autoCalcCalories': False, 'elevationCorrected':
# False, 'atpActivity': False, 'favorite': False, 'decoDive': False, 'parent': False}
