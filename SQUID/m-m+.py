import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math
import mpl_toolkits.axes_grid1.inset_locator as mpl_il

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

# Data directory
file = r"D:\MyData\CERN\OLD\R81-5\Mag Loop\M(H)_loop_81_5_5K_WholeLoop.dc.dat"
# file = r"D:\MyData\CERN\R183-5\SQUID\M(H)_loop_183_5_5K_WholeLoop.dc.dat"

title = "Nb$_3$Sn Thin Film, Sample 81-5, 5K"

# Constants
phi_0 = 2.067833848E-15  # Wb
mu_0 = 1.25663706212E-6
pi_value = math.pi
# Input sample dimension
a = 2802E-6
b = 2428E-6  # Smaller Than "a"
d = 2.67E-6

# Interval for x-axis (Field values)
interval_start = 0
interval_end = 67000

df = read_squid_data(file).loc[:, ['Field (Oe)', 'Long Moment (emu)']]

# df['Field (Oe)'] = -df['Field (Oe)']
# df['Long Moment (emu)'] = -df['Long Moment (emu)']

df['Field (Oe)'] = df['Field (Oe)']*1E-4

df = df[(df['Field (Oe)'] >= interval_start) & (df['Field (Oe)'] <= interval_end)]
df['rev'] = df.groupby("Field (Oe)")['Long Moment (emu)'].transform(
    lambda group: 1 * (((group.max() + group.min())) / 2)
    if len(group) > 1 
    else np.nan
)
df['irrev'] = df.groupby("Field (Oe)")['Long Moment (emu)'].transform(
    lambda group: 1 * (abs((group.max() - group.min())) / 2)
    if len(group) > 1 
    else np.nan
)

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Main plot
ax.scatter(df['Field (Oe)'], df['Long Moment (emu)'], linewidth=2, color="black", label="Experimental")
ax.plot(df['Field (Oe)'], df['rev'], marker="*", label="rev")
ax.plot(df['Field (Oe)'], df['irrev'], color="red", label="irrev")

# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax.set_xlabel("Field (T)", fontdict)
ax.set_ylabel("Long Moment (emu)", fontdict)

ax.set_title(title, fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.legend(prop=legend_font, loc='lower right')
plt.xlim(-0.005, 6.5)
plt.grid(True)

# Create inset of df['Field (Oe)'] vs. df['rev']
ax_inset = mpl_il.inset_axes(ax, width="45%", height="35%", loc='upper right')
ax_inset.plot(df['Field (Oe)'], df['rev'], marker="*", label="rev", color='green')
ax_inset.set_xlabel("Field (T)")
ax_inset.set_ylabel("Long Momnent (emu)", color='green')
ax_inset.tick_params(axis='y', labelcolor='green')
ax_inset.set_xlim(0, 6.5)
# ax_inset.set_ylim(-0.005, 0.005)
ax_inset.grid(True)
ax_inset.legend()

# # Create inset of df['Field (Oe)'] vs. df['rev']
# ax_inset = mpl_il.inset_axes(ax, width="30%", height="20%", loc='lower right')
# ax_inset.plot(df['Field (Oe)'], df['irrev'], marker="*", label="irrev", color='green')
# ax_inset.set_xlabel("Field (T)")
# ax_inset.set_ylabel("Long Momnent (emu)", color='green')
# ax_inset.tick_params(axis='y', labelcolor='green')
# ax_inset.set_xlim(0, 0.5)
# # ax_inset.set_ylim(-0.005, 0.005)
# ax_inset.grid(True)
# ax_inset.legend()

# Show both plots
# plt.tight_layout()

# plt.savefig(title+'rev.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title+'rev.png', format='png', bbox_inches='tight')

plt.show()
