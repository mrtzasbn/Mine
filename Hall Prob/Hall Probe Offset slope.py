import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Provide the file paths and labels
file_path = [
    (r'D:\Ramin\Nb3Sn\SHMP\R81_5\hc1_offset.dat', "0 to 1"),
    (r'D:\Ramin\Nb3Sn\SHMP\R81_5\hc2_offset.dat', "1 to -1"),
    (r'D:\Ramin\Nb3Sn\SHMP\R81_5\hc3_offset.dat', "-1 to 1")
]

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 8))


values_to_drop = [0, 4, -1.33850, -0.89900]
column_name = 'Field(T)'

hall_constant = []
labels = []
for file, label in file_path:
    labels.append(label)
    df = pd.read_csv(
        file, delim_whitespace=True, comment='#', header=None,
        names=['time(s)', 'Hall_Voltage(V)', 'Field(T)']
    )
    df = df[~(df[column_name].isin(values_to_drop))]
    hall_constant.append(df)


hall_constant1, hall_constant2, hall_constant3 = hall_constant
lable1, label2, label3 = labels

# ax.scatter(hall_constant1['Field(T)'], hall_constant1['Hall_Voltage(V)'], s = 50, color = "black", label=lable1)
# ax.scatter(hall_constant2['Field(T)'], hall_constant2['Hall_Voltage(V)'], s = 10,color = "black", label=label2)
ax.scatter(hall_constant3['Field(T)'], hall_constant3['Hall_Voltage(V)'], s = 10,color = "purple", label=label3)


# Define a list of intervals based on 'Field(T)' values
# intervals = [(-0.99, -0.54), (-0.54, -0.22), (-0.22, 0.02), (0.02, 0.29), (0.29, 0.50), (0.50, 0.99)]  # Define your desired intervals here
intervals = [(-1, -0.6), (-0.4, +0.4), (0.6, 1)]

# Define a function for the linear model
def linear(x, a, b):
    return a * x + b

# Create a single plot for all intervals
# ax.scatter(hall_constant3['Field(T)'], hall_constant3['Hall_Voltage(V)'], color= "black")

for interval in intervals:
    start_field, end_field = interval

    # Mask the data based on the interval
    masked_data = hall_constant3[(hall_constant3['Field(T)'] >= start_field) & (hall_constant3['Field(T)'] <= end_field)]

    x_interval = masked_data['Field(T)']
    y_interval = masked_data['Hall_Voltage(V)']

    params, _ = curve_fit(linear, x_interval, y_interval)

    x_data = np.linspace(start_field - 0.5, end_field + 0.5, 100)
    y_fit = linear(x_data, params[0], params[1])
    ax.plot(x_data, y_fit, label=f'Interval {interval}, slope=({-1/params[0]:.2f})', linestyle='--', linewidth=2)

    # Add vertical lines for interval boundaries
    # plt.axvline(x=start_field, color='red', linestyle='--')
    # plt.axvline(x=end_field, color='green', linestyle='--')

    # Annotate the value of params[0] in each interval
    # annotation_text = f'Slope: {-1/params[0]:.2f}'
    # ax.annotate(annotation_text, xy=(start_field, params[0] * start_field + params[1]), xytext=(start_field+0.1 , params[1] ),
    #               fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}, color='black')

# Find and plot intersection points
intersection_points = []

for i in range(len(intervals) - 1):
    start_field1, end_field1 = intervals[i]
    start_field2, end_field2 = intervals[i + 1]

    masked_data1 = df[(df['Field(T)'] >= start_field1) & (df['Field(T)'] <= end_field1)]
    masked_data2 = df[(df['Field(T)'] >= start_field2) & (df['Field(T)'] <= end_field2)]

    x_interval1 = masked_data1['Field(T)']
    y_interval1 = masked_data1['Hall_Voltage(V)']
    x_interval2 = masked_data2['Field(T)']
    y_interval2 = masked_data2['Hall_Voltage(V)']

    params1, _ = curve_fit(linear, x_interval1, y_interval1)
    params2, _ = curve_fit(linear, x_interval2, y_interval2)

    x_intersection = (params2[1] - params1[1]) / (params1[0] - params2[0])
    y_intersection = linear(x_intersection, params1[0], params1[1])

    intersection_points.append((x_intersection, y_intersection))

# Print or use the intersection points as needed
for i, point in enumerate(intersection_points):
    x, y = point
    print(f"Intersection {i + 1}: x = {x}, y = {y}")
    #  Annotate intersection points on the plot
    ax.annotate(f'({x:.2f})', (x, y), textcoords="offset points", xytext=(-20,-25), ha='center',
                 fontsize=15, color='black', fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'})
# Set font properties
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

# Set axis labels
ax.set_xlabel('Field(T)', fontdict)
ax.set_ylabel('Hall Voltage (V)', fontdict)

# Set tick fonts
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

# Add a legend
ax.legend(prop=legend_font)

# Show the plot
plt.show()
