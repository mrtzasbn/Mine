import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import interp1d
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

# Data directory
data_dir = r"D:\RawDataSquid\Nb3Sn\81-5\Mag_Loop"

# List of file paths and legend labels
data_info = [
    ("M(H)_loop_81_5_3K_WholeLoop.dc.dat", "3"),
    ("M(H)_loop_81_5_5K_WholeLoop.dc.dat", "5"),
    ("M(H)_loop_81_5_7K_WholeLoop.dc.dat", "7"),
    ("M(H)_loop_81_5_8K_WholeLoop.dc.dat", "8"),
    ("M(H)_loop_81_5_9K_WholeLoop.dc.dat", "9")
]

# Input sample dimension
a = 1860E-6
b = 1960E-6
d = 3E-6
coefficient = 4 / (a**2 * b * d * (1 - (a / (3 * b))))

# Interval for x-axis (Field values)
interval_start = 0
interval_end = 68500

# Create a DataFrame to store intersection points
intersection_results = pd.DataFrame(columns=["x", "y", "Temperature"])

# Magnetic Fields for intersection (T)
h_values = [
            # 0.01,
            0.05,
            # 0.1,
            # 0.25,
            # 0.5,
            # 1,
            # 2,
            # 3,
            # 5
            ]    

# Loop through each data file
for file_name, legend_label in data_info:
    # Construct the full file path
    file_path = os.path.join(data_dir, file_name)
    
    # Read SQUID data and select relevant columns
    df = read_squid_data(file_path).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
    num_indices = df.shape[0]

    # Divide dataset into increasing and decreasing field parts
    first_col = df['Field (Oe)'][:int(num_indices / 2)]
    second_col = df['Long Moment (emu)'][:int(num_indices / 2)]
    third_col = df['Long Moment (emu)'][int(num_indices / 2):][::-1].reset_index(drop=True)
    
    # Create a new DataFrame
    df_new = pd.DataFrame(
                        {
                        'Field': first_col,
                        'M+': second_col,
                        'M-': third_col
                        }
    )

    # Calculate Jc for the current data set
    df_new["Jc"] = 1E-3 * coefficient * abs((df_new["M+"] - df_new["M-"])) / 2
    
    # Mask the data based on the interval
    masked_data = df_new[(df_new['Field'] >= interval_start) & (df_new['Field'] <= interval_end)]

    # Interpolate the data
    interp_function = interp1d(masked_data['Field'] / 10000, masked_data['Jc'], kind='cubic')
    
    for h_value in h_values:
        # Calculate the corresponding y-values using interpolation
        y_intersection_value = interp_function(h_value)

        # Create a DataFrame for the current intersection point
        intersection_point = pd.DataFrame({
            "x": [h_value],
            "y": [y_intersection_value],
            "Temperature": [legend_label]
        })

        # Concatenate the intersection point DataFrame with intersection_results
        intersection_results = pd.concat([intersection_results, intersection_point], ignore_index=True)

# Pivot the intersection_results DataFrame
pivot_df = intersection_results.pivot(index="Temperature", columns="x", values="y")

# Save the pivot DataFrame to a CSV file
pivot_df.to_csv(os.path.join(data_dir, "pivot_results.csv"), index=True)

# Plot y data versus Temperature for different x values
x_values_to_plot = h_values  # Change this to the desired x values
# Plotting
fig, ax = plt.subplots()

for x_value in x_values_to_plot:
    y_data = pivot_df[x_value]
    ax.scatter(y_data.index, y_data.values,
            # marker='o',
            label=f'{x_value} T')

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax.set_xlabel("Temperature (K)", fontdict)
ax.set_ylabel("J$_c$ (A/m$^2$)", fontdict)
ax.set_title("J$_c$ values vs Temperature for different B values", fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.legend(prop=legend_font)
plt.show()


