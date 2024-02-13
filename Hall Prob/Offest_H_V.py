import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd




########################
def find_constant_intervals(x: np.ndarray, y: np.ndarray, delta=50E-7):
  constant_intervals = []
  current_interval = []
  for i in range(len(x)-1):
    if np.abs(y[i] - y[i+1]) < delta:
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
def mean_constant_function(x: np.ndarray, y: np.ndarray):
  mean_x = np.mean(x)
  mean_y = np.mean(y)
  return mean_x, mean_y

########################
def linear(x: np.ndarray, a, b):
    return a * x + b
########################
def linear_fit_intervals(intervals, x: np.ndarray, y: np.ndarray, ax=None):
  i=1
  for h_interval in intervals:
      # Mask the data based on the interval

      x_interval = x[(x >= h_interval[0]) & (x <= h_interval[1])]
      y_interval = y[(x >= h_interval[0]) & (x <= h_interval[1])]

      params, _ = curve_fit(linear, x_interval, y_interval)

      # Extend the x-data range for plotting
      if ax is not None:
        x_data = np.linspace(h_interval[0] - 0.2, h_interval[1] + 0.2, 100)  # Extend the range as needed
        y_fit = linear(x_data, params[0], params[1])
        ax.plot(x_data, y_fit, label=f'Slope {i}: {round(-1/params[0], 2)}', linestyle='--', linewidth=2)
      i +=1
  return params
########################
def intersections(intervals, x: np.ndarray, y: np.ndarray, linear_fit_function):
    intersection_points = []

    for i in range(len(intervals) - 1):
        start_field1, end_field1 = intervals[i]
        start_field2, end_field2 = intervals[i + 1]

        x_interval1 = x[(x >= start_field1) & (x <= end_field1)]
        y_interval1 = y[(x >= start_field1) & (x <= end_field1)]
        x_interval2 = x[(x >= start_field2) & (x <= end_field2)]
        y_interval2 = y[(x >= start_field2) & (x <= end_field2)]

        params1, _ = curve_fit(linear_fit_function, x_interval1, y_interval1)
        params2, _ = curve_fit(linear_fit_function, x_interval2, y_interval2)

        x_intersection = (params2[1] - params1[1]) / (params1[0] - params2[0])
        y_intersection = linear_fit_function(x_intersection, params1[0], params1[1])

        ax.axvline(x=x_intersection, color='red', linestyle='--')

        intersection_points.append((x_intersection, y_intersection))

    # Print or use the intersection points as needed
    for i, point in enumerate(intersection_points):
        x, y = point
        # print(f"Intersection {i + 1}: x = {x}, y = {y}")
        # Annotate intersection points on the plot
        ax.annotate(f'({x:.2f})', (x, y), textcoords="offset points", xytext=(-30, -10),
                     ha='center', color='black',
                     fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
                     )
    print(intersection_points)
    return intersection_points
########################
def subtract_data(x: np.ndarray, y: np.ndarray, slope: float, intercept: float, ax: plt.Axes = None):

  # Calculate the new y values based on the linear equation
  y_new = slope * x + intercept

  # Calculate the difference between the new y and the original y values
  sub = y_new - y

  # Plot the result if an Axes object is provided
  if ax is not None:
    ax.plot(x, sub, linestyle='-', linewidth=2, label='Subtraction Plot')
    # ax.legend()
    # ax.set_xlabel('x')
    # ax.set_ylabel('y_new - y')

  return sub
########################
# Load the data
file_path = r"F:\offset5K.dat"


df = pd.read_csv(
                file_path, delim_whitespace=True, comment='#', header=None,
                names=['time(s)', 'Hall_Voltage(V)', 'Field(T)']
                 )
df = df[(df['time(s)'] >= 1*1676) & (df['time(s)'] <= 3*1676)]

t = df['time(s)'].to_numpy()
v = df['Hall_Voltage(V)'].to_numpy()
h = df['Field(T)'].to_numpy()
########################

# Identify the intervals in which y is almost constant
constant_intervals = find_constant_intervals(t, v)

t_mean_values = []
v_mean_values = []
h_mean_values = []


for interval in constant_intervals:
  t_interval = t[(t >= interval[0]) & (t <= interval[1])]
  v_interval = v[(t >= interval[0]) & (t <= interval[1])]
  
  t_mean, v_mean = mean_constant_function(t_interval, v_interval)
  t_mean_values.append(t_mean)
  v_mean_values.append(v_mean)

################################################################################

for interval in constant_intervals:
  t_interval = t[(t >= interval[0]) & (t <= interval[1])]
  h_interval = h[(t >= interval[0]) & (t <= interval[1])]
  
  t_mean, h_mean = mean_constant_function(t_interval, h_interval)
  h_mean_values.append(h_mean)


t_mean_values = np.array(t_mean_values)
v_mean_values = np.array(v_mean_values)
h_mean_values = np.array(h_mean_values)


################################################################################

# Plot the results
fig, ax = plt.subplots(figsize=(10, 8))
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}


################################################################################

intervals = [(-0.9, -0.4), (-0.2, 0.2), (0.4, 0.9)]
linear_fit_intervals(intervals, h_mean_values, v_mean_values, ax=ax)

################################################################################

intersections(intervals, h_mean_values, v_mean_values, linear)

################################################################################


ax.scatter(h_mean_values, v_mean_values, label='Fitted Data', s=20, color = "black")

ax.set_xlabel('Field (T)', fontdict)
ax.set_ylabel('Hall Voltage (V)', fontdict)
plt.title("Hall Voltage while changing field\n from -1 T to 1 T", fontdict)

################################################################################

intervals = [(-0.2, 0.2)]
params = linear_fit_intervals(intervals, h_mean_values, v_mean_values,ax = None)
subtract_data(h_mean_values, v_mean_values, params[0],
              params[1], ax=ax)

ax.plot(h_mean_values, params[0] * np.array(h_mean_values) + params[1], label='Middle Fitted Area', linewidth=2, color = "purple", zorder=0)
################################################################################

# Set tick fonts
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)
plt.grid(True)
ax.legend(prop=legend_font)
# jpg_filename = "Offset-1to1New.jpg"
# plt.savefig(jpg_filename, format="jpg", dpi=300)
plt.show()
