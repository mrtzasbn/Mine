import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Provide the file path
file = [
    (r'D:\Data\SHMP\Nb3Sn ThinFilm\R81_5\Until 10 Nov 2023\hc1_fine_scan_5K_up_whole_rem.dat', "Before"),
    (r'D:\Data\SHMP\Nb3Sn ThinFilm\R81_5\Until 10 Nov 2023\hc2_fine_scan_5K_up_whole_rem.dat', "After")
        ]

title = ""

# Define a function for the Hall Constatnt Data
def hall_constant_data(file):
    hall_constant_data = pd.read_csv(
    file, delim_whitespace=True, comment='#', header=None,
    names=['time(s)', 'Hall_Voltage(V)', 'Field(T)']
                                )
    return hall_constant_data

# Define a function for the linear model
def linear(x, a, b):
    return a * x + b

def fit_in_intervals(hall_constant, intervals):
    hall_constant_values =[]
    for interval in intervals:
        start_field, end_field = interval

        # Mask the data based on the interval
        masked_data = hall_constant[(hall_constant['Field(T)'] >= start_field) & (hall_constant['Field(T)'] <= end_field)]

        x_interval = masked_data['Field(T)']
        y_interval = masked_data['Hall_Voltage(V)']

        params, _ = curve_fit(linear, x_interval, y_interval)

        hall_constant_values.append((-1/params[0]))

        x_data = np.linspace(start_field-0.5, end_field+0.5, 100)
        y_fit = linear(x_data, params[0], params[1])
        ax.plot(x_data, y_fit,
                #  label=f'Interval {interval}', linestyle='--'
                 )

        # Annotate the value of params[0] in each interval
        # annotation_text = f'Slope: {-1/params[0]:.2f}'
        # ax.annotate(annotation_text, xy=(start_field, params[0] * start_field + params[1]), xytext=(start_field+0.0015 , params[1] ),
        #             fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}, color='black')
    return hall_constant_values
     


# Define your desired intervals here


# Create a single plot for all intervals
fig, ax = plt.subplots(figsize=(10, 8))

# Read the data from the file, skipping lines starting with '#'
hall_data_frame = []
for file_path, label in file:
    hall_constant= hall_constant_data(file_path)
    hall_data_frame.append(hall_constant)
    ax.scatter(hall_constant['Field(T)'], hall_constant['Hall_Voltage(V)'], label=label)

intervals = [(0.01, 0.4), (0.6, 1.5)]

slope = []
for data in hall_data_frame:
    # slope = fit_in_intervals(data, intervals)
    slope.append(fit_in_intervals(data, intervals))
    
slope_mean1 = (slope[0][0]+slope[1][0])/2
slope_mean2 = (slope[0][1]+slope[1][1])/2

print(f"{slope_mean1:.2f}")
print(f"{slope_mean2:.2f}")



fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_xlabel("Field (T)", fontdict)
ax.set_ylabel('Hall Voltage (V)', fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

ax.legend(prop=legend_font)

plt.xlim(-0.1, 1.6)
plt.ylim(-0.04, 0.001)

plt.grid(True)
plt.show()
