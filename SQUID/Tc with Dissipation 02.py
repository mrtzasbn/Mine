import pandas as pd
import matplotlib.pyplot as plt
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


# Parameters
file = r"D:\MyData\CERN\R169-5\SQUID\Tc_0T.ac.dat"
title = "Susceptibility of Nb$_3$Sn Thin Film, Sample 169-5"

# Read SQUID data and extract relevant columns
df = read_squid_data(file).loc[:, ["Temperature (K)", "m' (emu)", 'm" (emu)', "m' Scan Std Dev", 'm" Scan Std Dev']]
df = df[(df['m" Scan Std Dev']<9.995E-7) & (df["m' Scan Std Dev"]<9.995E-6)]


# Create subplots
fig, ax = plt.subplots(figsize=(10, 8))
ax2 = ax.twinx()

# Create scatter plots
ax.scatter(df["Temperature (K)"], df["m' (emu)"], color="black", label="m' (emu)")
ax2.plot(df["Temperature (K)"], df['m" (emu)'], color="red", label='m" (emu)', marker='*')


# Set font styles
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

# Set labels and legend
ax.set_xlabel("Temperature (K)", fontdict)
ax.set_ylabel("m' (emu)", fontdict)
ax2.set_ylabel('m" (emu)', fontdict)

ax2.tick_params(axis='y')  # Tick color for secondary y-axis
ax.grid(True)
ax.set_title(title, fontdict)

# Set tick labels
for axis in [ax, ax2]:
    for tick in axis.get_xticklabels() + axis.get_yticklabels():
        tick.set(**tick_font)

# Combine legends from both axes
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, prop=legend_font, loc='upper left')
###################################################################
ax_inset = mpl_il.inset_axes(ax, width="50%", height="40%", loc='center')

# Read SQUID data and select relevant columns
ax_inset.scatter(df["Temperature (K)"], df["m' (emu)"], color="black", label="m' (emu)")
ax_inset.set_xlabel("Temperature (K)")
ax_inset.set_ylabel("m' (emu)", color='black')
# ax_inset.tick_params(axis='y', labelcolor='green')
# ax_inset.yaxis.set_label_position('right')
ax_inset.tick_params(axis='y', labelcolor='black')
# ax_inset.yaxis.tick_right()
# ax_inset.yaxis.set_ticks_position('both')
ax_inset.grid(True)
# ax_inset.legend()
inset_x_axis_start = 5
inset_x_axis_end = 16
inset_y_axis_start = -1.07E-4
inset_y_axis_end = -1.05E-4

ax_inset.set_xlim(inset_x_axis_start, inset_x_axis_end)
ax_inset.set_ylim(inset_y_axis_start, inset_y_axis_end)

######################################################################
a = 14
b = 16
# ax1.set_xlim(a, b)
# ax2.set_xlim(a, b)

plt.tight_layout()

# Save and display the plot
plt.savefig(title + '02.Tc.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title + '02.Tc.png', format='png', bbox_inches='tight')

# df.to_csv('title.csv', index=False)
plt.show()

