import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

# Function to read SQUID data and create a DataFrame
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df

# Define a function for the linear model
def linear(x, a, b):
    return a * x + b

# Parameters
file_path_infield = r"D:\MyData\CERN\R168-5\SQUID\KHM\Nb3Sn_Thin_Film_KHM_5K_infield.dc.dat"
file_path_rem = r"D:\MyData\CERN\R168-5\SQUID\KHM\Nb3Sn_Thin_Film_KHM_5K_rem.dc.dat"
title = "Nb$_3$Sn Thin Film, Sample 183-5, KHM Remnant"

df_infield = read_squid_data(file_path_infield).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
df_rem = read_squid_data(file_path_rem).loc[:, ['Field (Oe)', 'Long Moment (emu)']]



# Interpolate Long Moment values with a step of 1 in Field (Oe)
interp_func = interp1d(df_infield['Field (Oe)'], df_rem['Long Moment (emu)'], kind='cubic')
new_field = np.arange(df_infield['Field (Oe)'].min(), df_infield['Field (Oe)'].max() + 1, 1)
interpolated_long_moment = interp_func(new_field)

# Create new dataframe with interpolated values
interpolated_df = pd.DataFrame({'Field (Oe)': new_field,
                                'Long Moment (emu)': interpolated_long_moment})

fig, ax = plt.subplots(figsize=(10, 8))
ax2 = ax.twinx()

# Create scatter plots
ax.scatter(df_infield['Field (Oe)']/10, df_rem['Long Moment (emu)'], color="black", label="SQUID Data")
ax.plot(interpolated_df['Field (Oe)']/10, interpolated_df['Long Moment (emu)'], color="black")

# # Define interval
# interval = (0, 50)
# start, end = interval

# # Mask the data based on the interval
# masked_data = interpolated_df[(interpolated_df['Field (Oe)'] >= start) & (interpolated_df['Field (Oe)'] <= end)]
# x_interval = masked_data['Field (Oe)']
# y_interval = masked_data['Long Moment (emu)']

# # Fit linear model to the interval
# params, _ = curve_fit(linear, x_interval, y_interval)

# # Plot the fitted line for the interval
# x_data = interpolated_df['Field (Oe)']  # Generate X values within the interval range
# y_fit = linear(x_data, params[0], params[1])
# ax.plot(x_data/10, y_fit, color="red", label="Extrapolation")

# difference = (y_fit - interpolated_df['Long Moment (emu)'])
# ax2.plot(x_data/10, difference, linestyle='--', color="blue", label="Δ")

# # Find the index where the difference crosses the threshold value
# diff_sign = np.sign(difference.values + 0.00025)
# change_indices = np.where(diff_sign[:-1] != diff_sign[1:])[0]
# if len(change_indices) > 0:
#     first_index = change_indices[0] + 1
#     # ax2.plot(x_data[first_index]/10, difference.iloc[first_index], marker='o', markersize=8, color='red')
# else:
#     print("No sign change found.")
# plt.axvline(x=x_data[first_index]/10, color="green", linestyle='--')
# ax.annotate(
#         f'Start of Deviation: {x_data[first_index]/10:.2f} mT\n (difference = 0.00025)',
#         xy=(x_data[first_index]/10, difference.iloc[first_index]),
#         xytext=(x_data[first_index]/10-5, difference.iloc[first_index]+0.005),
#         fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
#     )


# Set font styles
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

# Set labels and legend
ax.set_xlabel('Field (mT)', fontdict)
ax.set_ylabel('Long Moment (emu)', fontdict)
ax2.set_ylabel('Δ (emu)', fontdict)
ax2.tick_params(axis='y')  # Tick color for secondary y-axis
ax.grid(True)
ax.set_title(title, fontdict)

# Set tick labels
for axis in [ax, ax2]:
    for tick in axis.get_xticklabels() + axis.get_yticklabels():
        tick.set(**tick_font)

# Combine legends from both axes
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, prop=legend_font, loc='upper right')

plt.tight_layout()

# Save and display the plot
# plt.savefig(title + '.KHM.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title + '.KHM.png', format='png', bbox_inches='tight')
plt.show()
