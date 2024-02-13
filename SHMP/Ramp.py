import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def hall_constant_data(file):
    hall_constant_data = pd.read_csv(
    file, delim_whitespace=True, comment='#', header=None,
    names=['time(s)', 'Hall_Voltage(V)', 'Field(T)']
                                )
    return hall_constant_data
# Define a function for the linear model
def linear(x, a, b):
    return a * x + b

# Provide the file path
file = r'D:\Data\CERN\R192-5\SHMP\Ramp\hc1_ramp2095.dat'
title = "Ramp for 2095"

# Read the data from the file, skipping lines starting with '#'
hall_constant = hall_constant_data(file)

offset = hall_constant['Hall_Voltage(V)'].iloc[0]
hall_constant_value = 46.46
hall_constant['Hall_Voltage(V)'] = (hall_constant['Hall_Voltage(V)']-offset)*hall_constant_value

# Define a list of intervals based on 'Field(T)' values
intervals = [(0, 0.01), (0.08, 0.1)]  # Define your desired intervals here

# Create a single plot for all intervals
fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(hall_constant['Field(T)']*1000, hall_constant['Hall_Voltage(V)']*1000, color= "black", label="Experimental")


results = []
for interval, (start_field, end_field) in enumerate(intervals):

    # Mask the data based on the interval
    masked_data = hall_constant[(hall_constant['Field(T)'] >= start_field) & (hall_constant['Field(T)'] <= end_field)]

    x_interval = masked_data['Field(T)']
    y_interval = masked_data['Hall_Voltage(V)']

    params, _ = curve_fit(linear, x_interval, y_interval)
    x_data = hall_constant['Field(T)']
    y_fit = linear(x_data, params[0], params[1])

    ax.plot(x_data*1000, y_fit*1000, linestyle='--', label=f"Fit, Slope: {params[0]:.2f}")
    results.append({'Interval': f'Interval {interval+1}', 'a': params[0], 'b': params[1]})

# Convert the list of dictionaries to a DataFrame
results_df = pd.DataFrame(results)
print(results_df)


# Determining the Intersection for each interval
intersection_points = []
for interval in range(len(intervals)-1):
    start_x, end_x = intervals[interval]
    x_intersection = (results_df["b"][interval] - results_df["b"][interval+1]) / (results_df["a"][interval+1] - results_df["a"][interval])
    y_intersection = results_df["a"][interval+1] * x_intersection + results_df["b"][interval+1]
    intersection_points.append({'Interval': f'Interval {interval+1}', 'Tc': x_intersection, 'Intersection': (x_intersection, y_intersection)})

# Plotting the Intersection
for point in intersection_points:
    ax.scatter(point["Intersection"][0]*1000, point["Intersection"][1]*1000, s=100, zorder=2)
    ax.annotate(
        f'Field$_i$$_n$$_t$: ({(point["Tc"])*1000:.2f} mT)',
        xy=point["Intersection"],
        xytext=(point["Intersection"][0]*1000-20, point["Intersection"][1]*1000+50),
        fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
    )


fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_xlabel("Applied Field (mT)", fontdict)
ax.set_ylabel('Measured Field (mT)', fontdict)
ax.set_title(title, fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

ax.legend(prop=legend_font)

plt.grid(True)

# plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title+'.png', format='png', bbox_inches='tight')
plt.show()
