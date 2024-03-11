import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1.inset_locator as mpl_il
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


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
file = [
    (r"D:\MyData\CERN\R169-5\SQUID\M(H)_loop_169_5_5K_WholeLoop.dc.dat", "169"),
    (r"D:\MyData\CERN\R86-5\SQUID\M(H)_loop_86_5_5K_WholeLoop.dc.dat", "86"),
    (r"D:\MyData\CERN\R94-4\SQUID\M(H)_loop_94_4_5K_WholeLoop.dc.dat", "94"),
    (r"D:\MyData\CERN\R168-5\SQUID\M(H)_loop_168_5_5K_WholeLoop.dc.dat", "168"),
    (r"D:\MyData\CERN\R173-5\SQUID\M(H)_loop_173_5_5K_WholeLoop.dc.dat", "173"),
    (r"D:\MyData\CERN\R183-5\SQUID\M(H)_loop_183_5_5K_WholeLoop.dc.dat", "183"),
    (r"D:\MyData\CERN\R192-5\SQUID\M(H)_loop_192_5_5K_WholeLoop.dc.dat", "192")
    

    
]





title = "Magnetization of Nb$_3$Sn, R169-5"


# Interval for x-axis (Field values)
interval_start = -80000
interval_end = 80000

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))
# Loop through each data file
for file_name, legend_label in file:
    # Read SQUID data and select relevant columns
    df = read_squid_data(file_name).loc[:, ['Field (Oe)', 'Long Moment (emu)', "Long Algorithm"]]
    max = df['Long Moment (emu)'].max()


    # Mask the data based on the interval
    masked_data = df[(df['Field (Oe)'] >= interval_start) & (df['Field (Oe)'] <= interval_end)]

    # Plotting Jc Field within the specified interval
    ax.plot(
        masked_data['Field (Oe)']/10000 ,
        masked_data['Long Moment (emu)'],
        # linewidth=2,
        # color= "black",
        label=legend_label,
        # s=2
    )



###################################################################
# ax_inset = mpl_il.inset_axes(ax, width="30%", height="20%", loc='upper left')
# for file_name, legend_label in file:
#     # Read SQUID data and select relevant columns
#     df = read_squid_data(file_name).loc[:, ['Field (Oe)', 'Long Moment (emu)', "Long Algorithm"]]
#     ax_inset.scatter(df['Field (Oe)']*1E-1, df['Long Moment (emu)'], marker = 'o', color='red', s=10)
# ax_inset.set_xlabel('Field (mT)')
# ax_inset.set_ylabel('Long Moment (emu)', color='black')
# # ax_inset.tick_params(axis='y', labelcolor='green')
# ax_inset.yaxis.set_label_position('right')
# ax_inset.tick_params(axis='y', labelcolor='black')
# ax_inset.yaxis.tick_right()
# # ax_inset.yaxis.set_ticks_position('both')
# ax_inset.grid(True)
# # ax_inset.legend()
# inset_x_axis_start = -6000
# inset_x_axis_end = 6000
# inset_y_axis_start = 0.28
# inset_y_axis_end = 0.38

# ax_inset.set_xlim(inset_x_axis_start*1E-1, inset_x_axis_end*1E-1)
# ax_inset.set_ylim(inset_y_axis_start, inset_y_axis_end)

######################################################################


# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax.set_xlabel("Field (T)", fontdict)
ax.set_ylabel("Long Moment (emu)", fontdict)
ax.set_title("Long Moment", fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.legend(prop=legend_font)

# Define the x and y-axis limits (Field values)
x_axis_start = -8000
x_axis_end = 8000
y_axis_start = -0.32
y_axis_end = -0.15

# plt.xlim(x_axis_start / 10000, x_axis_end / 10000)
# plt.ylim(y_axis_start, y_axis_end)

ax.set_title(title, fontdict)

plt.grid(True)
plt.tight_layout()

# # Saving the plot
# plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title+'.png', format='png', bbox_inches='tight')

# Display the plot
plt.show()