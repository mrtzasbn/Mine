import pandas as pd
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
hall_constant['Hall_Voltage(V)'] = (hall_constant['Hall_Voltage(V)'] - offset) * hall_constant_value

# Define a list of intervals based on 'Field(T)' values
interval = (0, 0.005)  # Define your desired intervals here

# Create a single plot for all intervals
fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(hall_constant['Field(T)']*1000, hall_constant['Hall_Voltage(V)']*1000, color="black", label="Hall Probe Data")

# Create a secondary y-axis
ax2 = ax.twinx()

start_field, end_field = interval

# Mask the data based on the interval
masked_data = hall_constant[(hall_constant['Field(T)'] >= start_field) & (hall_constant['Field(T)'] <= end_field)]

x_interval = masked_data['Field(T)']
y_interval = masked_data['Hall_Voltage(V)']

params, _ = curve_fit(linear, x_interval, y_interval)
x_data = hall_constant['Field(T)']
y_fit = linear(x_data, params[0], params[1])

ax.plot(x_data*1000, y_fit*1000, linestyle='--', color="r", label="Extrapolation")
# Plot the difference on the secondary y-axis
ax2.plot(x_data*1000, (y_fit - hall_constant['Hall_Voltage(V)'])*1000, linestyle='--', color="blue", label="Δ")



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
ax.legend(lines + lines2, labels + labels2, prop=legend_font, loc='upper left')

plt.grid(True)

# plt.savefig(title+'01.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title+'01.png', format='png', bbox_inches='tight')

plt.show()
