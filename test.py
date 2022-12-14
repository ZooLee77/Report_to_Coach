from fitparse import FitFile
import matplotlib.pyplot as plt
from statistics import mean
from scipy.signal import savgol_filter

fit_file = FitFile('8234833773_ACTIVITY.fit')

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


power = []
power_smoth = []
temp_smoth = []
breath = []
i = 0
temp_avarage = 0
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

yhat = savgol_filter(power, 151, 3) # window size 51, polynomial order 3
print(len(power))
print(len(power_smoth))
print(len(breath))

x = []
for i in range(len(breath)):
  x.append(i)

#plt.plot(x, power, color='green')
plt.plot(x, breath)
#plt.plot(x, yhat, color='red')
plt.show()