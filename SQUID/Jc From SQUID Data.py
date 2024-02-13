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

def groupby_squid_jc(file_path, coefficient, interval_start, interval_end, exception=70000):
    # Read SQUID data and select relevant columns
    df = read_squid_data(file_path).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
    if exception is None:
        df = df[df["Field (Oe)"]]
    else:
        df = df[df["Field (Oe)"] != exception]
    df = df[(df['Field (Oe)'] >= interval_start) & (df['Field (Oe)'] <= interval_end)]
    grouped_by  = df.groupby("Field (Oe)")
    df_new = grouped_by["Long Moment (emu)"].apply(
            lambda group: 1E-3 * coefficient * (abs((group.min() - group.max())) / 2)
            if len(group) > 1 
            else np.nan
        ).reset_index(name="Jc")
    return df_new



# Data directory
# List of file paths and legend labels
file = [
    (r"D:\MyData\CERN\R168-5\M(H)_loop_168_5_5K_WholeLoop.dc.dat", "5K"),
    # (r"D:\Data\SQUID Data\Nb3Sn ThinFilm\R81-5\Mag Loop\M(H)_loop_81_5_5K_WholeLoop.dc.dat", "6666K")
]


title= "J$_c^G$ of Nb$_3$Sn Thin Film, Sample 168-5, Thickness is missing!"

# Input sample dimension

# b_1 = 2432E-6
# b_2 = 2492E-6

# a_1 = 2376E-6
# a_2 = 2313E-6

# b = (b_1 + b_2)/2
# a = (a_1 + a_2)/2

a = 2462E-6
b = 2344.5E-6  # Smaller Than "a"
d = 2.7E-6

coefficient = 4 / (b**2 * a * d * (1 - (b / (3 * a))))

# Interval for x-axis (Field values)
interval_start = 0
interval_end = 70000

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Loop through each data file
for file_path, legend_label in file:

    df = groupby_squid_jc(file_path, coefficient, interval_start, interval_end,
                        #    exception=-70000
                           )

    # Find and annotate maximum Jc points
    max_jc = (df['Jc'].max())/1E10
    max_field = (df.loc[df['Jc'].idxmax(), 'Field (Oe)']) / 10000

    if len(file) == 1:
        color = "black"
    else:
        color = None
    ax.scatter(df["Field (Oe)"]/10000, df["Jc"]/1E10, label=legend_label, color=color)





    # ax.scatter(
    #         max_field, max_jc, marker='o', s=150, color="red"
    #         # label=f"J$_c$ $_M$$_a$$_x$ ({legend_label})"
    # )

    # ax.annotate(
    #     f'J$_c^G$ $_M$$_a$$_x$: ({max_field:.2f} T, {max_jc:.2f} $\\times 10^{{{10}}}$ A/m$^2$))',
    #     xy=(max_field, max_jc),
    #     xytext=(max_field + 0.5, max_jc + 0.1),
    #     fontproperties={'family': 'serif', 'size': 14, 'weight': 'regular'}
    # )

# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax.set_xlabel("Field (T)", fontdict)
ax.set_ylabel("J$_c^G$ ($\\times 10^{{{:d}}}$ A/m$^2$)".format(10), fontdict)

ax.set_title(title, fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.legend(prop=legend_font)

# # Display the plot
plt.grid(True)
plt.tight_layout()


plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title+'.png', format='png', bbox_inches='tight')
plt.show()
