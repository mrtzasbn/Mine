import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math
# Function to read SQUID data and create a DataFrame
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df


# Define a function for the linear model
def linear(x, a, b):
    return a * x + b
################################################################
# Data directory
file = r"D:\MyData\CERN\R183-5\SQUID\M(H)_loop_183_5_11K_HighFields.dc.dat"
# file = r"D:\MyData\CERN\R183-5\SQUID\M(H)_loop_183_5_5K_WholeLoop.dc.dat"

title= "Nb$_3$Sn Thin Film, Sample 183-5, 11K"
################################################################
# Constants
phi_0 = 2.067833848E-15  # Wb
mu_0  = 1.25663706212E-6
pi_value = math.pi
# Input sample dimension
a = 2275E-6
b = 2143E-6
d = 2.717E-6
d_cu = 495E-6
v = a * b * d
v_cu = a * b * d_cu
cu_suceptibility = -5.46E-6*1E-6
################################################################
# Interval for x-axis (Field values)
interval_start = 0
interval_end = 68000
################################################################
df = read_squid_data(file).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
df['Field (Oe)'] = df['Field (Oe)']*1E-4
# df['Field (Oe)'] = -df['Field (Oe)']
# df['Long Moment (emu)'] = -df['Long Moment (emu)']

df["cu"] = df["Field (Oe)"]*cu_suceptibility/mu_0
################################################################
df = df[(df['Field (Oe)'] >= interval_start) & (df['Field (Oe)'] <= interval_end)]
df['rev'] = df.groupby("Field (Oe)")['Long Moment (emu)'].transform(
    lambda group: 1 * (((group.max() + group.min())) / 2)
    if len(group) > 1 
    else np.nan
)

df["rev-cu"] = df["rev"] - df["cu"]
df["Field (Oe)"] = np.log(df["Field (Oe)"])
################################################################
# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# ax.scatter(df['Field (Oe)'] , df['Long Moment (emu)'], linewidth=2, color= "black", label="Experimental")

ax.plot(df['Field (Oe)'], df['rev'], marker="*", label="m$_-$ + m$_+$")
ax.plot(df['Field (Oe)'], df['cu'], color= "red", label="Cu")
ax.plot(df['Field (Oe)'], df['rev-cu'], color= "green", marker="o")

################################################################
interval = (1.6, 2)
start, end = interval
masked_data = df[(df['Field (Oe)'] >= start) & (df['Field (Oe)'] <= end)]

x_interval = masked_data['Field (Oe)']
y_interval = masked_data['rev-cu']*1E-3/v

params, _ = curve_fit(linear, x_interval, y_interval)

x_data =df['Field (Oe)']
y_fit = linear(x_data, params[0], params[1])
# ax.plot(x_data, y_fit, label="Fitted Line", linewidth=2, color="red")
print(params)
################################################################

# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax.set_xlabel("Field (Oe)", fontdict)
ax.set_ylabel("M A/m", fontdict)

# ax.set_title(title, fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.legend(prop=legend_font)


plt.grid(True)
plt.tight_layout()


# plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title+'.png', format='png', bbox_inches='tight')
plt.show()
