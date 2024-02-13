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
file = r'D:\MyData\CERN\R192-5\SHMP\hc1_upper_edge_fine_5K_infield_ramp.dat'

# Read the data from the file, skipping lines starting with '#'
hall_constant = hall_constant_data(file)

# Define a list of intervals based on 'Field(T)' values
intervals = [(0, 0.1)]  # Define your desired intervals here



# Create a single plot for all intervals
fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(hall_constant['Field(T)'], hall_constant['Hall_Voltage(V)'], color= "black")

for interval in intervals:
    start_field, end_field = interval

    # Mask the data based on the interval
    masked_data = hall_constant[(hall_constant['Field(T)'] >= start_field) & (hall_constant['Field(T)'] <= end_field)]

    x_interval = masked_data['Field(T)']
    y_interval = masked_data['Hall_Voltage(V)']

    params, _ = curve_fit(linear, x_interval, y_interval)
    print(1/params[0], params[1])

    x_data = np.linspace(start_field-0.003, end_field+0.003, 100)
    y_fit = linear(x_data, params[0], params[1])
    ax.plot(x_data, y_fit, label=f'Interval {interval}', linestyle='--')

    # Add vertical lines for interval boundaries
    plt.axvline(x=start_field, color='red', linestyle='--')
    plt.axvline(x=end_field, color='green', linestyle='--')

    # Annotate the value of params[0] in each interval
    annotation_text = f'Slope: {1/params[0]:.2f}'
    ax.annotate(annotation_text, xy=(start_field, params[0] * start_field + params[1]), xytext=(start_field+0.0015 , params[1] ),
                  fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}, color='black')

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

plt.grid(True)
plt.show()
