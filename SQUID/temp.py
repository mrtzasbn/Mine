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

# Function to create scatter plot
def create_scatter_plot(ax, x_data, y_data, color="black", label=None):
    ax.scatter(x_data, y_data, color=color, label=label)

# File path and title
file = r"D:\Data\CERN\Thinfilm\Nb3Sn\R192-5\AC-5K_Field_R192-5_High.ac.dat"
title = "Nb$_3$Sn Thin Film, Sample 192-5"

# Read data and group by 'Field (Oe)' while calculating mean
df = read_squid_data(file).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)']]
df_grouped = df.groupby("Field (Oe)")[["m' (emu)", 'm" (emu)']].mean()

# Create a scatter plot for 'Field (Oe)' vs "m' (emu)"
fig, ax1 = plt.subplots()
create_scatter_plot(ax1, df_grouped.index, df_grouped["m' (emu)"], color="blue", label="m' (emu)")
ax1.set_xlabel('Field (Oe)')
ax1.set_ylabel("m' (emu)", color="blue")
ax1.tick_params(axis='y', labelcolor="blue")
ax1.set_title(title)

# Create a scatter plot for 'Field (Oe)' vs 'm" (emu)'
ax2 = ax1.twinx()
create_scatter_plot(ax2, df_grouped.index, df_grouped['m" (emu)'], color="red", label='m" (emu)')
ax2.set_ylabel('m" (emu)', color="red")
ax2.tick_params(axis='y', labelcolor="red")

# Show the legend
fig.tight_layout()
fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

# Display the plot
plt.show()
