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

# Parameters
file = r"D:\MyData\CERN\R86-5\Tc_0T.ac.dat"


# Read SQUID data and extract relevant columns
df = read_squid_data(file).loc[:, ["Temperature (K)", "m' (emu)", 'm" (emu)', "m' Scan Std Dev", 'm" Scan Std Dev']]
df = df[(df['m" Scan Std Dev']<9.99E-7) & (df["m' Scan Std Dev"]<9.99E-7)]
df["m' (emu)"] = df["m' (emu)"]*1E-3
df['m" (emu)'] = df['m" (emu)']*1E-3
# df['m" (emu)'] = 0


interval = (5, 8)

df = df[(df["Temperature (K)"]>=interval[0]) & (df["Temperature (K)"]<=interval[1])]

df["sus"] = np.sqrt(df['m" (emu)']**2 + df["m' (emu)"]**2)

mean = df["sus"].mean()
slope = mean/(0.3*1E-4)
print(f"{slope:.4e}")







# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
ax = (ax1, ax2)

# Create scatter plots
ax1.scatter(df["Temperature (K)"], df["m' (emu)"], color="black")
ax2.scatter(df["Temperature (K)"], df['m" (emu)'], color="black")

# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax2.set_xlabel("Temperature (K)", fontdict)
ax1.set_ylabel("m' (emu)", fontdict)
ax2.set_ylabel('m" (emu)', fontdict)

# ax1.set_title(title, fontdict)

# Set tick labels
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for i in ax:
        for tick in i.get_xticklabels():
            tick.set(**tick_font)
        for tick in i.get_yticklabels():
            tick.set(**tick_font)

# Add grid
ax1.grid(True)
ax2.grid(True)

a = 14
b = 16
# ax1.set_xlim(a, b)
# ax2.set_xlim(a, b)

plt.tight_layout()

plt.show()

