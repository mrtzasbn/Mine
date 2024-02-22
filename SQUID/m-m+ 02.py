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
file = r"D:\MyData\CERN\R173-5\SQUID\M(H)_loop_173_5_11K_HighFields.dc.dat"
filecu = r"D:\MyData\CERN\R173-5\SQUID\M(H)_loop_173_5_22K.dc.dat"

title = "Nb$_3$Sn Thin Film, Sample 173-5 with Cu, 11K"


# Interval for x-axis (Field values)
interval_start = 0
interval_end = 70000

df = read_squid_data(file).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
df['Field (Oe)'] = df['Field (Oe)']*1E-4

df = df[(df['Field (Oe)'] >= interval_start) & (df['Field (Oe)'] <= interval_end)]
df['rev'] = df.groupby("Field (Oe)")['Long Moment (emu)'].transform(
    lambda group: 1 * (((group.max() + group.min())) / 2)
    if len(group) > 1 
    else np.nan
)

df_cu  = read_squid_data(filecu).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
df_cu['Field (Oe)'] = df_cu['Field (Oe)']*1E-4


# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Main plot
ax.plot(df['Field (Oe)'], df['rev'], marker="*", label="rev")
ax.plot(df_cu['Field (Oe)'], df_cu['Long Moment (emu)'], marker="+", label="cu")


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
ax.legend(prop=legend_font)

plt.grid(True)



# Show both plots
plt.tight_layout()

plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title+'.png', format='png', bbox_inches='tight')

plt.show()
