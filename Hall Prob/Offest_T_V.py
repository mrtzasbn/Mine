import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.ticker as ticker


file_path = r"F:\offset5K.dat"


df = pd.read_csv(
                file_path, delim_whitespace=True, comment='#', header=None,
                names=['time(s)', 'Hall_Voltage(V)', 'Field(T)']
                 )

########################
def find_constant_intervals(x, y):
  constant_intervals = []
  current_interval = []
  for i in range(len(x)-1):
    if np.abs(y[i] - y[i+1]) < 50E-7:
      current_interval.append(x[i])
    else:
      if len(current_interval) > 0:
        constant_intervals.append((current_interval[0], current_interval[-1]))
      current_interval = []

  # Add the last constant interval, even if it is not followed by a point that is different from the first point.
  if len(current_interval) > 0:
    constant_intervals.append((current_interval[0], current_interval[-1]))

  return constant_intervals
########################
def mean_constant_function(x, y):
  mean_x = np.mean(x)
  mean_y = np.mean(y)
  return mean_x, mean_y
########################

# Load the data

x = df['time(s)'].to_numpy()
y = df['Hall_Voltage(V)'].to_numpy()
z = df['Field(T)'].to_numpy()
########################

# Identify the intervals in which y is almost constant
constant_intervals = find_constant_intervals(x, y)

x_mean_values = []
y_mean_values = []
z_mean_values = []


for interval in constant_intervals:
  x_interval = x[(x >= interval[0]) & (x <= interval[1])]
  y_interval = y[(x >= interval[0]) & (x <= interval[1])]
  
  x_mean, y_mean = mean_constant_function(x_interval, y_interval)
  x_mean_values.append(x_mean)
  y_mean_values.append(y_mean)

################################################################################


for interval in constant_intervals:
  x_interval = x[(x >= interval[0]) & (x <= interval[1])]
  z_interval = z[(x >= interval[0]) & (x <= interval[1])]
  
  x_mean, z_mean = mean_constant_function(x_interval, z_interval)
  z_mean_values.append(z_mean)


################################################################################
# Plot the results

fig, ax = plt.subplots(figsize=(10, 8))


ax.scatter(x, y, label='Data', s=50, color = "blue")
ax.scatter(x_mean_values, y_mean_values, label='Fitted Data', s=20, color = "red")
# plt.scatter(y_mean_values, z_mean_values, label='fit', s=10, color = "red")



################################################################################

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_xlabel('Time (s)', fontdict)
ax.set_ylabel('Hall Voltage (V)', fontdict)


# plt.title("Hall Voltage between changing field [0.5, -0.5] and back", fontdict)

# Set tick fonts
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

plt.grid(True)

ax.legend(prop=legend_font)

jpg_filename = "Offset01.jpg"
plt.savefig(jpg_filename, format="jpg", dpi=300)
plt.show()
