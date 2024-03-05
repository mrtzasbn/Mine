import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1.inset_locator as mpl_il
import matplotlib.ticker as ticker

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



fig, ax = plt.subplots(figsize=(10, 8))

# Plot 'Value' against index for each group
for name, group in grouped:
    max = group['m" (emu)'].max()
    ax.plot(group.reset_index(drop=True).index + 1, group.reset_index(drop=True)['m" (emu)']/max, label=f'Field {int(name)/10} (mT)', marker = 'o', color="black")

for name02, group02 in grouped02:
    max = group02['m" (emu)'].max()
    ax.plot(group02.reset_index(drop=True).index + 1, group02.reset_index(drop=True)['m" (emu)']/max, label=f'Field {int(name02)/10} (mT), 10 min', marker = '*')

for name03, group03 in grouped03:
    max = group03['m" (emu)'].max()
    ax.plot(group03.reset_index(drop=True).index + 1, group03.reset_index(drop=True)['m" (emu)']/max, label=f'Field {int(name03)/10} (mT), 1 Hz', marker = '+')



# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_title('m" (emu) vs  AC tries', fontdict)
ax.set_xlabel('Try', fontdict)
# ax.set_ylabel('m" $\\times 10^{{{-6}}}$ (emu)', fontdict)
ax.set_ylabel('m" (Normalized)', fontdict)
ax.legend(prop=legend_font)

# Set tick labels
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

ax.grid(True)

plt.savefig("actries" + '01moretry.pdf', format='pdf', bbox_inches='tight')
plt.savefig("actries" + '01moretry.png', format='png', bbox_inches='tight')

plt.show()




