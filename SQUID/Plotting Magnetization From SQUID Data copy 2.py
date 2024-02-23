import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate

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
file = r"D:\MyData\CERN\R183-5\SQUID\M(H)_loop_183_5_5K_WholeLoop.dc.dat"

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

df = read_squid_data(file).loc[:, ['Field (Oe)', 'Long Moment (emu)', "Long Algorithm"]]
chanck = int(len(df['Field (Oe)']) / 4)
df1 = df.iloc[1*chanck+0:2*chanck+2, :]
df2 = df.iloc[2*chanck+2:3*chanck+2, :]

# Linear interpolation
x = df1['Field (Oe)'].values
y = df1['Long Moment (emu)'].values
f = interpolate.interp1d(x, y, kind='linear')
x_new = df2['Field (Oe)'].values
df2['Interpolated Long Moment (emu)'] = f(x_new)

# Scatter plot for df1
ax.scatter(
    df1['Field (Oe)'] / 10000,
    df1['Long Moment (emu)'],
    color="black",
    label='df1'
)

# Scatter plot for df2
ax.scatter(
    df2['Field (Oe)'] / 10000,
    df2['Long Moment (emu)'],
    color="red",
    label='df2'
)

# Plot interpolated data
ax.scatter(
    df2['Field (Oe)'] / 10000,
    df2['Interpolated Long Moment (emu)'],
    color='blue',
    # linestyle='--',
    label='Interpolated df2'
)

# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax.set_xlabel("Field (T)", fontdict)
ax.set_ylabel("Long Moment (Normalized)", fontdict)
ax.set_title("Long Moment", fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.legend(prop=legend_font)


plt.grid(True)
plt.tight_layout()

# Display the plot
plt.show()
