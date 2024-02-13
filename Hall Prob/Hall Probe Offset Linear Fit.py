import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


file_path = r"F:\OffsetData.dat"
file_encoding = 'utf-8'  # Adjust the encoding if needed

# Read the data from the file into a DataFrame, skipping lines that start with #
df = pd.read_csv(file_path, delim_whitespace=True, comment='#', header=None, names=[
    'time(s)', 'field(T)', 'V_hall(V)', 'V_dms(V)', 'temp(K)', 'temp_VTI(K)', 
    'heater_setpoint(K)', 'heater_power(%)', 'heater_range(id)', 'He(%)', 'x(µm)', 'y(µm)', 'z(µm)'
], encoding=file_encoding)

df['time(s)'] = df['time(s)']-1699007156.426
df = df[(df['time(s)'] >= 2265) & (df['time(s)'] <= 3790)]
df
fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(df['field(T)'], df['V_hall(V)'], color = "black", s=10)
############################################################
# Define a list of intervals based on 'Field(T)' values
intervals = [[-0.48, -0.35], (-0.1, 0.1), [0.35, 0.48]]  # Define your desired intervals here

# Define a function for the linear model
def linear(x, a, b):
    return a * x + b


for interval in intervals:
    start_field, end_field = interval

    # Mask the data based on the interval
    df_masked_data = df[(df['field(T)'] >= start_field) & (df['field(T)'] <= end_field)]

    x_interval = df_masked_data['field(T)']
    y_interval = df_masked_data['V_hall(V)']

    params, _ = curve_fit(linear, x_interval, y_interval)

    x_data = np.linspace(start_field-0.3, end_field+0.3, 100)
    y_fit = linear(x_data, params[0], params[1])
    ax.plot(x_data, y_fit, label=f'Interval {interval}', linestyle='--', linewidth=2)

intersection_points = []

for i in range(len(intervals) - 1):
    start_field1, end_field1 = intervals[i]
    start_field2, end_field2 = intervals[i + 1]

    masked_data1 = df[(df['field(T)'] >= start_field1) & (df['field(T)'] <= end_field1)]
    masked_data2 = df[(df['field(T)'] >= start_field2) & (df['field(T)'] <= end_field2)]

    x_interval1 = masked_data1['field(T)']
    y_interval1 = masked_data1['V_hall(V)']
    x_interval2 = masked_data2['field(T)']
    y_interval2 = masked_data2['V_hall(V)']

    params1, _ = curve_fit(linear, x_interval1, y_interval1)
    params2, _ = curve_fit(linear, x_interval2, y_interval2)

    x_intersection = (params2[1] - params1[1]) / (params1[0] - params2[0])
    y_intersection = linear(x_intersection, params1[0], params1[1])

    plt.axvline(x=x_intersection, color='red', linestyle='--')
    
    intersection_points.append((x_intersection, y_intersection))

print(intersection_points)

# Print or use the intersection points as needed
for i, point in enumerate(intersection_points):
    x, y = point
    print(f"Intersection {i + 1}: x = {x}, y = {y}")
    #  Annotate intersection points on the plot
    ax.annotate(f'({x:.2f})', (x, y), textcoords="offset points", xytext=(-30,-10),
                 ha='center', color='black',
                 fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
                 )

############################################################
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

# Set axis labels
ax.set_xlabel('Field (T)', fontdict)
ax.set_ylabel('Hall Voltage (V)', fontdict)

plt.title("Hall Voltage between changing field -0.5 to 0.5", fontdict)

# Set tick fonts
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)
plt.xlim(-0.51, 0.51)
plt.ylim(-0.011, 0.011)
plt.grid(True)


plt.show()

