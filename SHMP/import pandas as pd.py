import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import numpy as np

def hall_constant_data(file):
    hall_constant_data = pd.read_csv(
        file, delim_whitespace=True, comment='#', header=None,
        names=['time(s)', 'Hall_Voltage(V)', 'Field(T)']
    )
    return hall_constant_data

def sg_filter_1d(y, window_size, order, deriv=0):
    try:
        window_size = abs(int(window_size))
        order = abs(int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")

    if window_size % 2 != 1 or window_size < 1:
        raise ValueError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise ValueError("window_size is too small for the polynomials order")

    order_range = list(range(order+1))
    half_window = (window_size - 1) // 2

    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * (10**deriv)

    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])

    y = np.concatenate((firstvals, y, lastvals))

    return np.convolve( m[::-1], y, mode='valid')

# Provide the file path
file = r'D:\MyData\CERN\R192-5\SHMP\Ramp\hc1_ramp2100.dat'
title = "Ramp for 2100"

# Read the data from the file, skipping lines starting with '#'
hall_constant = hall_constant_data(file)

offset = hall_constant['Hall_Voltage(V)'].iloc[0]
hall_constant_value = 46.46
hall_constant['Hall_Voltage(V)'] = (hall_constant['Hall_Voltage(V)'] - offset) * hall_constant_value

hall_voltage = hall_constant['Hall_Voltage(V)'].values
field = hall_constant['Field(T)'].values

# Use Savitzky-Golay filter to smooth the Hall voltage data
smoothed_hall_voltage = sg_filter_1d(hall_voltage, window_size=5, order=3)

# Use interpolation to interpolate hall_voltage based on field values
interp_function = interp1d(field, smoothed_hall_voltage, kind='linear')

# Generate new field values for interpolation covering the entire range of field values
new_field_values = np.linspace(min(field), max(field), len(field))

# Interpolate hall_voltage for the new field values
interpolated_hall_voltage = interp_function(new_field_values)

# Calculate the derivative of the smoothed Hall voltage with respect to field
derivative = np.gradient(interpolated_hall_voltage, new_field_values)

# Plotting the original data, the smoothed data, and its derivative
fig, ax = plt.subplots(figsize=(10, 8))
# ax.plot(field, hall_voltage, color="black", label="Original Hall Voltage")
# ax.plot(new_field_values, smoothed_hall_voltage, color="blue", label="Smoothed Hall Voltage")
ax.plot(new_field_values, derivative, color="red", label="Derivative of Smoothed Hall Voltage")

# Labeling and styling the plot
ax.set_xlabel('Field (T)')
ax.set_ylabel('Hall Voltage (V), Derivative')
ax.legend()
plt.grid(True)
plt.title(title)
plt.show()
