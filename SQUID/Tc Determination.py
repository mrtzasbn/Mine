import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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

def tc_data(file_path):
    tc = read_squid_data(file_path).loc[:, ["Temperature (K)", "m' (emu)", 'm" (emu)']]
    return tc

file = r"D:\MyData\CERN\R94-4\SQUID\Tc_7T.ac.dat"
# title = "T$_c$ vs Field, R94-4, First deviation from Linear in Dissipation, 7T"
title = "$_c$ vs Field, R94-4, Intersection of Fitting, 7T"
intervals = [
    # (16.9, 17.5),
    # (13, 14.5),
    (9.86, 10.84),
    (11.68, 13.5),
    
]

df = tc_data(file)

results = []
for interval, (start, end) in enumerate(intervals):
    # Mask the data based on the interval
    masked_data = df[(df["Temperature (K)"] >= start) & (df["Temperature (K)"] <= end)]

    x_interval = masked_data["Temperature (K)"]
    y_interval = masked_data["m' (emu)"]

    params, _ = curve_fit(linear, x_interval, y_interval)
    # Append the results to the list as a dictionary
    results.append({'Interval': f'Interval {interval+1}', 'a': params[0], 'b': params[1]})

# Convert the list of dictionaries to a DataFrame
results_df = pd.DataFrame(results)

# Determining the Intersection for each interval
intersection_points = []
for interval in range(len(intervals)-1):
    start_x, end_x = intervals[interval]
    x_intersection = (results_df["b"][interval] - results_df["b"][interval+1]) / (results_df["a"][interval+1] - results_df["a"][interval])
    y_intersection = results_df["a"][interval+1] * x_intersection + results_df["b"][interval+1]
    intersection_points.append({'Interval': f'Interval {interval+1}', 'Tc': x_intersection, 'Intersection': (x_intersection, y_intersection)})

# Print the intersection points for each interval
for point in intersection_points:
    print(f'{point["Interval"]}: Tc = {point["Tc"]:.2f} K, Intersection = {point["Intersection"]}')

# Plot the original data
fig, ax = plt.subplots(figsize=(10, 8))

ax.scatter(
    df["Temperature (K)"],
    df["m' (emu)"],
    marker="o",
    color="black",
    label="Exp. Data"
)

# Plot the fitted lines for each interval
for interval, (start_x, end_x) in enumerate(intervals):
    x_data = np.linspace(start_x-1, end_x+1, 100)  # Generate X values within the interval range
    y_fit = linear(x_data, results_df.at[interval, 'a'], results_df.at[interval, 'b'])
    ax.plot(x_data, y_fit,
            # label=f'Linear Fit {interval + 1}'
            )

# Plotting the Intersection
for point in intersection_points:
    ax.scatter(point["Intersection"][0], point["Intersection"][1], s=100, zorder=2)
    ax.annotate(
        f'T$_i$$_n$$_t$: ({point["Tc"]:.2f} K)',
        xy=point["Intersection"],
        xytext=(point["Intersection"][0] - 1.5, point["Intersection"][1] + 1E-6),
        fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
    )

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.set_xlabel("Temperature (K)", fontdict)
ax.set_ylabel("m' (emu)", fontdict)
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

    
ax.legend(prop=legend_font)

ax.set_title(title, fontdict)

# plt.xlim(13, 18.1)
plt.ylim(df["m' (emu)"].min()+(df["m' (emu)"].min())/10, df["m' (emu)"].max()-(df["m' (emu)"].min())/10)
# plt.ylim(df['m" (emu)'].min()+(df['m" (emu)'].min())/10, df['m" (emu)'].max()-(df['m" (emu)'].min())/10)
plt.grid(True)

plt.savefig(title + 'Fit01.TcDet.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title + 'Fit01.TcDet.png', format='png', bbox_inches='tight')

plt.show()
