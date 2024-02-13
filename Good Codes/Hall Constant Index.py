import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Provide the file path
file_path = r'D:\Ramin\Nb3Sn\SHMP\R81_5\hc1_fine_scan_5K_up_whole_rem.dat'

# Read the data from the file, skipping lines starting with '#'
hall_constant = pd.read_csv(
                file_path, delim_whitespace=True, comment='#', header=None,
                names=['time(s)', 'Hall_Voltage(V)', 'Field(T)']
                 )


num_indices = hall_constant.shape[0]


int1 = hall_constant['Field(T)'][int(0.25*num_indices)]
int2 = hall_constant['Field(T)'][int(0.753*num_indices)]
# int1 = hall_constant['Field(T)'][7]
# int2 = hall_constant['Field(T)'][10]
interval = [int1, int2]

# Define a function for the linear model
def linear(x, a, b):
        return a * x + b


for start, end in enumerate(interval):
    # Mask the data based on the interval
    masked_data = hall_constant[(hall_constant['Field(T)'] >= start) & (hall_constant['Field(T)'] <= end)]

    x_interval = masked_data['Field(T)']
    y_interval = masked_data['Hall_Voltage(V)']

    params, _ = curve_fit(linear, x_interval, y_interval)


print(f"Hall Constant is {-1/params[0]}")


fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(hall_constant['Field(T)'], hall_constant['Hall_Voltage(V)'])


x_data = np.linspace(int1, int2, 100)
y_fit = linear(x_data, params[0], params[1])
ax.plot(x_data, y_fit, c="r")

plt.axvline(x=int1, color='red', linestyle='--')
plt.axvline(x=int2, color='green', linestyle='--')




fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}


ax.set_xlabel("Field (T)", fontdict)
ax.set_ylabel('Hall Voltage (V)', fontdict)

plt.title(f"The Hall Constant is {-1/params[0]:.2f} T/V", fontdict)
          
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

# ax.legend(prop=legend_font)
# fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}

plt.show()