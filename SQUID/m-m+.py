import pandas as pd
import matplotlib.pyplot as plt
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




# Data directory
file = r"D:\MyData\CERN\R183-5\SQUID\M(H)_loop_183_5_11K_HighFields.dc.dat"
# file = r"D:\MyData\CERN\R183-5\SQUID\M(H)_loop_183_5_5K_WholeLoop.dc.dat"

title= "Nb$_3$Sn Thin Film, Sample 183-5, 11K"

# Input sample dimension
a = 2275E-6
b = 2143E-6
d = 2.717E-6
d_cu = 495E-6
v = a * b * d
v_cu = a * b * d_cu


# Interval for x-axis (Field values)
interval_start = 0
interval_end = 68000

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

df = read_squid_data(file).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
df['Field (Oe)'] = df['Field (Oe)']*1E-4
# df['Field (Oe)'] = -df['Field (Oe)']
# df['Long Moment (emu)'] = -df['Long Moment (emu)']

df = df[(df['Field (Oe)'] >= interval_start) & (df['Field (Oe)'] <= interval_end)]
df1 = df.groupby("Field (Oe)")['Long Moment (emu)'].apply(
            lambda group: 1 * (((group.max() + group.min())) / 2)
            if len(group) > 1 
            else np.nan
        ).reset_index()
df1.rename(columns={'Long Moment (emu)': 'Delta'}, inplace=True)

df2 = df.groupby("Field (Oe)")['Long Moment (emu)'].apply(
            lambda group: 1 * (((group.max() - group.min())) / 2)
            if len(group) > 1 
            else np.nan
        ).reset_index()
df2.rename(columns={'Long Moment (emu)': 'Delta'}, inplace=True)
ax.plot(df1['Field (Oe)'], df1['Delta'], marker="*", label="m$_-$ + m$_+$")

ax.plot(df2['Field (Oe)'], df2['Delta'], marker="+", label="m$_-$ - m$_+$")

ax.scatter(
        df['Field (Oe)'] ,
        df['Long Moment (emu)'],
        linewidth=2,
        color= "black",
        label="Experimental"
    )



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
