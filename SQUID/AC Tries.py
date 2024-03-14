import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1.inset_locator as mpl_il
import matplotlib.ticker as ticker
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
file =   r"D:\MyData\IS258A\AC-5K_IS258A_High_80mT.ac.dat"
file02 = r"D:\MyData\IS258A\AC-5K_IS258A_High_80mT_FC.ac.dat"
# file03 = r"D:\MyData\IS258A\AC-77K_IS258A_High_80mT.ac.dat"

title= "IS258, more AC"

df = read_squid_data(file).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit", "Time"]]
# df = df[df["Regression Fit"] > 9.999E-1]
df.loc[df["Regression Fit"] <= 9.995E-1, ['m" (emu)']] = np.nan
grouped = df.groupby("Field (Oe)")

df2 = read_squid_data(file02).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit", "Time"]]
# df2 = df2[df2["Regression Fit"] > 9.999E-1]
df2.loc[df2["Regression Fit"] <= 9.995E-1, ['m" (emu)']] = np.nan
grouped02 = df2.groupby("Field (Oe)")

# df3 = read_squid_data(file03).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit", "Time"]]
# df3 = df3[df3["Regression Fit"] > 9.999E-1]
# df3.loc[df3["Regression Fit"] <= 9.999E-1, ['m" (emu)']] = np.nan

# grouped03 = df3.groupby("Field (Oe)")



fig, ax = plt.subplots(figsize=(10, 8))

# Plot 'Value' against index for each group
for name, group in grouped:
    
    # min = group['m" (emu)'].min()
    min = 0
    # max = group['m" (emu)'].max()-min
    max = 1
    ax.plot(group.reset_index(drop=True).index + 1, ((group.reset_index(drop=True)['m" (emu)']-min)/max)*1E6, label=f'Field {int(name)/10} (mT).', marker = 'o', color="black")

for name02, group02 in grouped02:
    
    # min = group02['m" (emu)'].min()
    min = 0
    # max = group02['m" (emu)'].max()-min
    max = 1 
    ax.plot(group02.reset_index(drop=True).index + 1, ((group02.reset_index(drop=True)['m" (emu)']-min)/max)*1E6, label=f'Field {int(name02)/10} (mT), FC', marker = '*')




ax_inset = mpl_il.inset_axes(ax, width="40%", height="30%", loc='center right')

for name02, group02 in grouped02:

    # min = group03['m" (emu)'].min()
    min = 0
    # max = group03['m" (emu)'].max()-min
    max = 1
    ax_inset.plot(group02.reset_index(drop=True).index + 1, ((group02.reset_index(drop=True)['m" (emu)']-min)/max)*1E6, label=f'Field {int(name02)/10} (mT), FC', marker = '+')
ax_inset.set_xlabel("Try")
ax_inset.set_ylabel('m" $\\times 10^{{{-6}}}$ (emu)')
ax_inset.tick_params(axis='y')
ax_inset.grid(True)
ax_inset.legend()













# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_title('m" (emu) vs  AC tries, 5K', fontdict)
ax.set_xlabel('Try', fontdict)
ax.set_ylabel('m" $\\times 10^{{{-6}}}$ (emu)', fontdict)
# ax.set_ylabel('m" (Normalized)', fontdict)
ax.legend(prop=legend_font)

# Set tick labels
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

ax.grid(True)

plt.savefig("AC_" + '.pdf', format='pdf', bbox_inches='tight')
plt.savefig("AC_" + '.png', format='png', bbox_inches='tight')

plt.show()




