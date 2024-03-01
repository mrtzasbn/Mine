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



# List of file paths and legend labels
file = r"D:\MyData\CERN\R94-4\SQUID\AC Modified 02\AC-5K_Field_R94-5_High_Modified02.ac.dat"
file02 = r"D:\MyData\CERN\R94-4\SQUID\AC Modified 03\AC-5K_Field_R94-5_High_Modified02.ac.dat"
title= "Sample 94-4, more AC"

df = read_squid_data(file).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit"]]
grouped = df.groupby("Field (Oe)")

df2 = read_squid_data(file02).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit"]]
grouped02 = df2.groupby("Field (Oe)")



fig, ax = plt.subplots(figsize=(10, 8))

# Plot 'Value' against index for each group
for name, group in grouped:
    ax.plot(group.reset_index(drop=True)['m" (emu)'], label=f'Field {int(name)/10} (mT)', marker = 'o')

for name01, group01 in grouped02:
    ax.plot(group01.reset_index(drop=True)['m" (emu)'], label=f'Field {int(name01)/10} (mT), High Frequency', marker = '*')




ax_inset = mpl_il.inset_axes(ax, width="40%", height="30%", loc='center left')
for name, group in grouped:
    ax_inset.plot(group.reset_index(drop=True)['m" (emu)'], label=f'Field {int(name)/10} (mT)', marker = 'o')
ax_inset.set_xlabel("Try")
ax_inset.set_ylabel('m" (emu)', color='green')
ax_inset.tick_params(axis='y', labelcolor='green')
ax_inset.grid(True)
ax_inset.legend()

ax_inset = mpl_il.inset_axes(ax, width="40%", height="30%", loc='center right')
for name01, group01 in grouped02:
    ax_inset.plot(group01.reset_index(drop=True)['m" (emu)'], label=f'Field {int(name)/10} (mT), High Frequency', marker = 'o')
ax_inset.set_xlabel("Try")
ax_inset.set_ylabel('m" (emu)', color='green')
ax_inset.tick_params(axis='y', labelcolor='green')
ax_inset.grid(True)
ax_inset.legend()
















# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_title('m" (emu) vs  AC tries', fontdict)
ax.set_xlabel('Try', fontdict)
ax.set_ylabel('m" (emu)', fontdict)
ax.legend(prop=legend_font)

# Set tick labels
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

ax.grid(True)

plt.savefig("actries" + '02.pdf', format='pdf', bbox_inches='tight')
plt.savefig("actries" + '02.png', format='png', bbox_inches='tight')

plt.show()




