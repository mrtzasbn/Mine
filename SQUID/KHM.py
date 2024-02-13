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
def create_scatter_plot(ax, x_data, y_data, color="black"):
    ax.scatter(x_data, y_data, color=color)

# Parameters
file_path_infield = r"D:\MyData\CERN\R168-5\KHM\Nb3Sn_Thin_Film_KHM_5K_infield.dc.dat"
file_path_rem = r"D:\MyData\CERN\R168-5\KHM\Nb3Sn_Thin_Film_KHM_5K_rem.dc.dat"
title = "Nb$_3$Sn Thin Film, Sample 168-5"

df_infield = read_squid_data(file_path_infield).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
df_rem = read_squid_data(file_path_rem).loc[:, ['Long Moment (emu)']]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
ax = (ax1, ax2)

# Create scatter plots
create_scatter_plot(ax1, df_infield['Field (Oe)']/10, df_infield['Long Moment (emu)'])
create_scatter_plot(ax2, df_infield['Field (Oe)']/10, df_rem['Long Moment (emu)'])

# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
# legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax2.set_xlabel('Field (mT)', fontdict)
ax1.set_ylabel('Long Moment (emu)', fontdict)
ax2.set_ylabel('Long Moment (emu)', fontdict)

ax1.set_title("Infield", fontdict)
ax2.set_title("Remnant", fontdict)

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
plt.savefig(title + '.KHM.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title + '.KHM.png', format='png', bbox_inches='tight')
plt.show()