import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

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
file = r'D:\MyData\CERN\R192-5\SHMP\Ramp\hc1_ramp2090.dat'
title = "Ramp for 2090"

# Read the data from the file, skipping lines starting with '#'
hall_constant = hall_constant_data(file)

offset = hall_constant['Hall_Voltage(V)'].iloc[0]
hall_constant_value = 46.12
hall_constant['Hall_Voltage(V)'] = (hall_constant['Hall_Voltage(V)'] - offset) * hall_constant_value

# Define a list of intervals based on 'Field(T)' values
# interval = (0, 0.005)  # Define your desired intervals here
intervals = [
    # (12, 14.9),
    # (15, 15.6),
    (0, 0.01),
    (0.08, 0.1)
]
# Create a single plot for all intervals
fig, ax = plt.subplots(figsize=(10, 8))
ax2 = ax.twinx()
# Retrieve the default color cycle
colors = ax._get_lines.prop_cycler

ax.plot(hall_constant['Field(T)']*1000, hall_constant['Hall_Voltage(V)']*1000, color="black", label="Hall Probe Data")

results = []
for interval, (start, end) in enumerate(intervals):

    # Mask the data based on the interval
    masked_data = hall_constant[(hall_constant['Field(T)'] >= start) & (hall_constant['Field(T)'] <= end)]

    x_interval = masked_data['Field(T)']
    y_interval = masked_data['Hall_Voltage(V)']

    params, _ = curve_fit(linear, x_interval, y_interval)
    x_data = hall_constant['Field(T)']
    y_fit = linear(x_data, params[0], params[1])

    ax.plot(x_data*1000, y_fit*1000, linestyle='--', label=f"Extrapolation, Slope: {params[0]:.2f}", color=next(colors)['color'])
    results.append({'Interval': f'Interval {interval+1}', 'a': params[0], 'b': params[1]})

    # Plot the difference on the secondary y-axis
    difference = (y_fit - hall_constant['Hall_Voltage(V)']) * 1000  # Multiply by 1000 to convert to mT
    # ax2.plot(x_data*1000, difference, linestyle='--', label=f"Δ {interval+1}", color=next(colors)['color'])
    
    # Find the index where the difference crosses the threshold value
    diff_sign = np.sign(difference.values - 1)
    first_index = np.where(diff_sign[:-1] != diff_sign[1:])[0][0] + 1
    # Plot a marker on the first point where the difference crosses the threshold
    # ax2.plot(x_data[first_index]*1000, difference.iloc[first_index], marker='o', markersize=8, color='red')


    plt.axvline(x=x_data[first_index]*1000, color=next(colors)['color'], linestyle='--')
    # ax.annotate(
    #     f'Start of Deviation: ({x_data[first_index]*1000:.2f} mT)',
    #     xy=(x_data[first_index]*1000, difference.iloc[first_index]),
    #     xytext=(x_data[first_index]*1000-20, difference.iloc[first_index]+50),
    #     fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
    # )




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
# for point in intersection_points:
#     ax.scatter(point["Intersection"][0]*1000, point["Intersection"][1]*1000, s=100, zorder=2)
#     ax.annotate(
#         f'Field$_i$$_n$$_t$: ({(point["Tc"])*1000:.2f} mT)',
#         xy=point["Intersection"],
#         xytext=(point["Intersection"][0]*1000-20, point["Intersection"][1]*1000+50),
#         fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
#     )




fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_xlabel("Applied Field (mT)", fontdict)
ax.set_ylabel('Measured Field (mT)', fontdict)
ax.set_title(title, fontdict)

ax2.set_ylabel('Δ (mT)', fontdict)  # Secondary y-axis label
ax2.tick_params(axis='y')  # Tick color for secondary y-axis

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)
for tick in ax2.get_yticklabels():
    tick.set(**tick_font)

# Combine legends from both axes
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, prop=legend_font, loc='upper center')
ax.set_xlim(0, 25)
ax.set_ylim(0, 150)

plt.grid(True)

plt.savefig(title+'All.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title+'All.png', format='png', bbox_inches='tight')

plt.show()
