import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1.inset_locator as mpl_il
import numpy as np

# Function to read SQUID data and create a DataFrame
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df



# List of file paths and legend labels
file =   r"D:\MyData\CERN\R86-5\AC Modified\80mT\AC-5K_Field_R86-5_High_ModifiedMoreAC80mT.ac.dat"
file02 = r"D:\MyData\CERN\R86-5\AC Modified\80mT\AC-5K_Field_R86-5_High_ModifiedMoreAC10min80mT.ac.dat"
file03 = r"D:\MyData\CERN\R86-5\AC Modified\80mT\AC-5K_Field_R86-5_High_ModifiedMoreAC1Hz80mT.ac.dat"
file04 = r"D:\MyData\CERN\R86-5\AC Modified\30mT\AC-5K_Field_R86-5_High_ModifiedMoreAC30mT.ac.dat"
title= "Sample 86-5, more AC"

df = read_squid_data(file).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit", "Time"]]
df = df[df["Regression Fit"] > 9.999E-1]
grouped = df.groupby("Field (Oe)")

df2 = read_squid_data(file02).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit", "Time"]]
df2 = df2[df2["Regression Fit"] > 9.999E-1]
grouped02 = df2.groupby("Field (Oe)")

df3 = read_squid_data(file03).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit", "Time"]]
df3 = df3[df3["Regression Fit"] > 9.999E-1]
grouped03 = df3.groupby("Field (Oe)")

df4 = read_squid_data(file04).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit", "Time"]]
df4 = df4[df4["Regression Fit"] > 9.999E-1]
grouped04 = df4.groupby("Field (Oe)")

fig, ax = plt.subplots(figsize=(10, 8))

for name, group in grouped:
    zero_time = group["Time"].iloc[0]  # Get the zero time for this specific group
    group["Time"] = group["Time"] - zero_time  # Modify Time for this group only
    ax.plot(np.log(group["Time"]/60), group['m" (emu)']*1E+6, label=f'Field {int(name)/10} (mT)', marker='o', color="black")

for name02, group02 in grouped02:
    zero_time = group02["Time"].iloc[0]
    group02["Time"] = group02["Time"] - zero_time
    ax.plot(np.log(group02["Time"]/60), group02['m" (emu)']*1E+6, label=f'Field {int(name02)/10} (mT), 10 min', marker='*')
# for name, group in grouped:
#     zero_time = group["Time"].iloc[0]  # Get the zero time for this specific group
#     group["Time"] = group["Time"] - zero_time  # Modify Time for this group only
#     ax.plot(group["Time"]/60, group['m" (emu)']*1E+6, label=f'Field {int(name)/10} (mT)', marker='o', color="black")

# for name02, group02 in grouped02:
#     zero_time = group02["Time"].iloc[0]
#     group02["Time"] = group02["Time"] - zero_time
#     ax.plot((group02["Time"]/60), group02['m" (emu)']*1E+6, label=f'Field {int(name02)/10} (mT), 10 min', marker='*')

# for name03, group03 in grouped03:
#     zero_time = group03["Time"].iloc[0]
#     group03["Time"] = group03["Time"] - zero_time
#     ax.plot(group03["Time"]/60, group03['m" (emu)']*1E+6, label=f'Field {int(name03)/10} (mT), 1 Hz', marker='+')

# for name04, group04 in grouped04:
#     zero_time = group04["Time"].iloc[0]
#     group04["Time"] = group04["Time"] - zero_time
#     ax.plot(group04["Time"]/60, group04['m" (emu)']*1E+6, label=f'Field {int(name04)/10} (mT)', marker='h')


# ax_inset = mpl_il.inset_axes(ax, width="40%", height="30%", loc='center right')

# for name04, group04 in grouped04:
#     zero_time = group04["Time"].iloc[0]
#     group04["Time"] = group04["Time"] - zero_time
#     ax_inset.plot(group04["Time"]/60, group04['m" (emu)']*1E+6, label=f'Field {int(name04)/10} (mT)', marker='h')
# ax_inset.set_xlabel("Time (min)")
# ax_inset.set_ylabel('m" $\\times 10^{{{-6}}}$ (emu)')
# ax_inset.tick_params(axis='y')
# ax_inset.grid(True)
# ax_inset.legend()

# ax_inset = mpl_il.inset_axes(ax, width="40%", height="30%", loc='upper center', bbox_to_anchor=(-0.1, 0, 1, 1), bbox_transform=ax.transAxes)
# for name04, group04 in grouped03:
#     zero_time = group03["Time"].iloc[0]
#     group03["Time"] = group03["Time"] - zero_time
#     ax_inset.plot(group03["Time"]/60, group03['m" (emu)']*1E+6, label=f'Field {int(name03)/10} (mT), 1 Hz', marker='+')
# ax_inset.set_xlabel("Time (min)")
# ax_inset.set_ylabel('m" $\\times 10^{{{-6}}}$ (emu)')
# ax_inset.tick_params(axis='y')
# ax_inset.grid(True)
# ax_inset.legend()

# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_title('m" (emu) vs  AC tries', fontdict)
ax.set_xlabel('Time (min)', fontdict)
ax.set_ylabel('m" $\\times 10^{{{-6}}}$ (emu)', fontdict)
ax.legend(prop=legend_font)

# Set tick labels
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

ax.grid(True)

# plt.savefig("actries" + '80mT01.pdf', format='pdf', bbox_inches='tight')
# plt.savefig("actries" + '80mT01.png', format='png', bbox_inches='tight')

plt.show()




