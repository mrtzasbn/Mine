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
file = [
    (r"D:\MyData\CERN\R183-5\SQUID\M(H)_loop_183_5_5K_WholeLoop.dc.dat", "5K"),
    # (r"D:\MyData\CERN\R168-5\M(H)_loop_168_5_8K_HighFields.dc.dat", "8K"),
    # (r"D:\MyData\CERN\R168-5\M(H)_loop_168_5_11K_HighFields.dc.dat", "11K"),
    # (r"D:\MyData\CERN\R168-5\M(H)_loop_168_5_14K_HighFields.dc.dat", "14K"),
    # (r"D:\Data\SQUID Data\Nb3Sn ThinFilm\R81-5\Mag Loop\M(H)_loop_81_5_9K_WholeLoop.dc.dat", "9K"),

    
]





title = "Magnetization of Nb$_3$Sn, Sample 168-5"


# Interval for x-axis (Field values)
interval_start = -80000
interval_end = 80000

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))
# Loop through each data file
for file_name, legend_label in file:
    # Read SQUID data and select relevant columns
    df = read_squid_data(file_name).loc[:, ['Field (Oe)', 'Long Moment (emu)']]

    # Mask the data based on the interval
    masked_data = df[(df['Field (Oe)'] >= interval_start) & (df['Field (Oe)'] <= interval_end)]

    # Plotting Jc Field within the specified interval
    ax.scatter(
        masked_data['Field (Oe)']/10000 ,
        masked_data['Long Moment (emu)'],
        # linewidth=2,
        # color= "black",
        label=legend_label
    )



# Indication line for specific situations 
# plt.axvline(x=400/10000, color='red', linestyle='--')


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