import pandas as pd
import matplotlib.pyplot as plt


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
file = r"D:\MyData\CERN\R94-4\SQUID\AC Modified 02\AC-5K_Field_R94-5_High_Modified01.ac.dat"
title= "Nb$_3$Sn Thin Film, Sample 173-5, Low Field"

df = read_squid_data(file).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit"]]
# df = df[df["Regression Fit"]>9.9E-1]
# df  = df.groupby("Field (Oe)")[["m' (emu)", 'm" (emu)']].mean().reset_index()

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
ax = (ax1, ax2)


# Scatter plot for 'Field (Oe)' vs "m' (emu)"
ax1.plot(df['Field (Oe)']/10, df["m' (emu)"], color="blue", label="m' (emu)", marker="o")
# Scatter plot for 'Field (Oe)' vs 'm" (emu)'
ax2.plot(df['Field (Oe)']/10, df['m" (emu)'], color="red", label='m" (emu)', marker="o")

# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
# legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax2.set_xlabel("Field (mT)", fontdict)
ax1.set_ylabel("m' (emu)", fontdict)
ax2.set_ylabel('m" (emu)', fontdict)

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

plt.tight_layout()
# Save and display the plot
# plt.savefig(title + 'Low.AC.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title + 'Low.AC.png', format='png', bbox_inches='tight')
plt.show()



