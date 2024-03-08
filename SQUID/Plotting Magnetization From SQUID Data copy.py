import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Function to read SQUID data and create a DataFrame
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df


def linear(x, a, b):
    return a * x + b

# List of file paths and legend labels
file = r"D:\MyData\CERN\R86-5\M(H)_loop_86_5_5K_Meissner.dc.dat"
df = read_squid_data(file).loc[:, ['Field (Oe)', 'Long Moment (emu)', "Long Algorithm"]]
df['Long Moment (emu)'] = df['Long Moment (emu)']*1E-3
df['Field (Oe)'] = df['Field (Oe)']*1E-4

interval = (0, 0.025) # Tesla

masked_data = df[(df['Field (Oe)']>=interval[0]) & (df['Field (Oe)']<=interval[1])]

x_data = masked_data['Field (Oe)']
y_data = masked_data['Long Moment (emu)']


params, _ = curve_fit(linear, x_data, y_data)

print(f"{params[0]:.4e}")
print(f"{params[1]:.4e}")

df['delta'] = df['Long Moment (emu)'] - linear(df['Field (Oe)'], params[0], params[1])
    
print(df)
fig, ax = plt.subplots(figsize=(10, 8))
######################################################################
# Plotting Jc Field within the specified interval
ax.scatter(df['Field (Oe)']*1E3 , df['Long Moment (emu)'], color= "black")
ax.plot(df['Field (Oe)']*1E3, linear(df['Field (Oe)'], params[0], params[1]), color="red")
ax.plot(df['Field (Oe)']*1E3, df['delta'], color="blue")
######################################################################


# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax.set_xlabel("Applied Field (mT)", fontdict)
ax.set_ylabel("Magnetic Moment (Am$^2$)", fontdict)
# ax.set_title("Long Moment", fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
# ax.legend(prop=legend_font)

# Define the x and y-axis limits (Field values)
x_axis_start = -8000
x_axis_end = 8000
y_axis_start = df['Long Moment (emu)'].min() + 0.05*(df['Long Moment (emu)'].min())

# plt.xlim(x_axis_start / 10000, x_axis_end / 10000)
# plt.ylim(y_axis_start, 0.00002)

# ax.set_title(title, fontdict)

plt.grid(True)
plt.tight_layout()

# # Saving the plot
# plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title+'.png', format='png', bbox_inches='tight')

# Display the plot
plt.show()