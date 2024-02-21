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

# Numerical differentiation function
def numerical_derivative(x, y):
    dy_dx = np.gradient(y, x)
    return dy_dx

# Parameters
file = r"D:\Data\CERN\R183-5\SQUID\Tc_0T.ac.dat"
title = "T$_c$ of Nb$_3$Sn Thin Film, Sample 168-5"

# Read SQUID data and extract relevant columns
df = read_squid_data(file).loc[:, ["Temperature (K)", "m' (emu)", 'm" (emu)', "m' Scan Std Dev", 'm" Scan Std Dev']]
df = df[(df['m" Scan Std Dev']<9.99E-7) & (df["m' Scan Std Dev"]<9.99E-7)]

# Calculate derivative of m' (emu) with respect to Temperature
df['dm_dT'] = numerical_derivative(df["Temperature (K)"], df["m' (emu)"])

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
ax = (ax1, ax2)

# Create scatter plots
ax1.scatter(df["Temperature (K)"], df["m' (emu)"], color="black", label="m' (emu)")
ax2.scatter(df["Temperature (K)"], df['dm_dT'], color="blue", label="dm'/dT")

# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax2.set_xlabel("Temperature (K)", fontdict)
ax1.set_ylabel("m' (emu)", fontdict)
ax2.set_ylabel("dm'/dT", fontdict)
ax1.set_title(title, fontdict)

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

# Add legend
ax1.legend()
ax2.legend()

plt.tight_layout()

# Save and display the plot
plt.show()
