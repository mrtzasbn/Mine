import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

# Provide the file paths and labels
file_path = [
    (r'D:\Data\SHMP\R81_5\hc2_offset.dat', "1 to -1"),
    (r'D:\Data\SHMP\R81_5\hc3_offset.dat', "-1 to 1")
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

hall_constant1, hall_constant2 = hall_constant

# Sort both dataframes by the 'Field(T)' column
df1 = hall_constant1.sort_values(by='Field(T)')
df2 = hall_constant2.sort_values (by='Field(T)')

x1_values1 = hall_constant1['Field(T)'].values
y1_values1 = hall_constant1['Hall_Voltage(V)'].values
x2_values2 = hall_constant2['Field(T)'].values

# Create an interpolation function (linear interpolation)
interpolation_function = interp1d(x1_values1, y1_values1, kind='linear', fill_value="extrapolate")
interpolated_y1 = interpolation_function(x2_values2)

# Create a new dataframe to store the interpolated values
interpolated_data = {'Field(T)': x2_values2, 'Hall_Voltage(V)': interpolated_y1}
hall_constant1 = pd.DataFrame(interpolated_data)

# Display the interpolated dataframe
df = pd.merge(hall_constant1, hall_constant2, how="left", on="Field(T)")
df["diff"] = abs(df["Hall_Voltage(V)_x"] - df["Hall_Voltage(V)_y"])

ax.scatter(df['Field(T)'], df["diff"], s=50)

# Define a list of intervals based on 'Field(T)' values
intervals = [(-0.9, -0.51), (-0.47, -0.25), (-0.22, -0.04), (0.04, 0.27), (0.31, 0.53), (0.51, 1)]  # Define your desired intervals here

# Define a function for the linear model
def linear(x, a, b):
    return a * x + b

# Create a single plot for all intervals
for interval in intervals:
    start_field, end_field = interval

    # Mask the data based on the interval
    masked_data = df[(df['Field(T)'] >= start_field) & (df['Field(T)'] <= end_field)]

    x_interval = masked_data['Field(T)']
    y_interval = masked_data["diff"]

    params, _ = curve_fit(linear, x_interval, y_interval)

    # Extend the x-data range for plotting
    x_data = np.linspace(start_field - 0.1, end_field + 0.1, 100)  # Extend the range as needed
    y_fit = linear(x_data, params[0], params[1])
    ax.plot(x_data, y_fit, label=f'Interval {interval}', linestyle='--')

    # Add vertical lines for interval boundaries
    # plt.axvline(x=start_field, color='red', linestyle='--')
    # plt.axvline(x=end_field, color='green', linestyle='--')



# Find and plot intersection points
intersection_points = []

for i in range(len(intervals) - 1):
    start_field1, end_field1 = intervals[i]
    start_field2, end_field2 = intervals[i + 1]

    masked_data1 = df[(df['Field(T)'] >= start_field1) & (df['Field(T)'] <= end_field1)]
    masked_data2 = df[(df['Field(T)'] >= start_field2) & (df['Field(T)'] <= end_field2)]

    x_interval1 = masked_data1['Field(T)']
    y_interval1 = masked_data1["diff"]
    x_interval2 = masked_data2['Field(T)']
    y_interval2 = masked_data2["diff"]

    params1, _ = curve_fit(linear, x_interval1, y_interval1)
    params2, _ = curve_fit(linear, x_interval2, y_interval2)

    x_intersection = (params2[1] - params1[1]) / (params1[0] - params2[0])
    y_intersection = linear(x_intersection, params1[0], params1[1])

    plt.axvline(x=x_intersection, color='black', linestyle='--')
    
    intersection_points.append((x_intersection, y_intersection))

# Print or use the intersection points as needed
for i, point in enumerate(intersection_points):
    x, y = point
    print(f"Intersection {i + 1}: x = {x}, y = {y}")
    #  Annotate intersection points on the plot
    ax.annotate(f'({x:.2f})', (x, y), textcoords="offset points", xytext=(-30,-10),
                 ha='center', color='black',
                 fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
                 )



# Set font properties
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

# Set axis labels
ax.set_xlabel('Field(T)', fontdict)
ax.set_ylabel('\u0394 Hall Voltage (V)', fontdict)

plt.title("Difference between changing field from\n1 to -1 and -1 to 1", fontdict)

# Set tick fonts
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)
# Add a legend
# ax.legend(prop=legend_font)

# Show the plot
plt.show()
