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



# List of file paths and legend labels
file = r"D:\MyData\CERN\R192-5\SQUID\AC-5K_Field_R192-5_High.ac.dat"
title= "Nb$_3$Sn Thin Film, Sample 183-5, High Field"

df = read_squid_data(file).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit"]]
df = df[df["Regression Fit"]>9.999E-1]

df  = df.groupby("Field (Oe)")[["m' (emu)", 'm" (emu)']].mean().reset_index()

intervals = [

    (0, 100),
    (400, 900)
]

results = []

for interval, (start, end) in enumerate(intervals):
    # Mask the data based on the interval
    masked_data = df[(df['Field (Oe)'] >= start) & (df['Field (Oe)'] <= end)]

    x_interval = masked_data['Field (Oe)']
    y_interval = masked_data['m" (emu)']

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
    intersection_points.append({'Interval': f'Interval {interval+1}', 'int': x_intersection, 'Intersection': (x_intersection/10, y_intersection)})

# Print the intersection points for each interval
for point in intersection_points:
    print(f'{point["Interval"]}: int = {point["int"]/10:.2f} mT, Intersection = {point["Intersection"]}')

# Plot the original data
fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(
    df['Field (Oe)']/10,
    df['m" (emu)'],
    marker="+",
    color="black",
    # label="Exp. Data"
)

# Plot the fitted lines for each interval
for interval, (start_x, end_x) in enumerate(intervals):
    x_data = df['Field (Oe)']  # Generate X values within the interval range
    y_fit = linear(x_data, results_df.at[interval, 'a'], results_df.at[interval, 'b'])
    ax.plot(x_data/10, y_fit,
            linewidth=3
            )


# Plotting the Intersection
for point in intersection_points:
    ax.scatter(point["Intersection"][0], point["Intersection"][1], s=100, zorder=2, color="r")
    ax.annotate(
        f'Field$_i$$_n$$_t$: ({point["int"]/10:.2f} mT)',
        xy=point["Intersection"],
        xytext=(point["Intersection"][0]-25 , point["Intersection"][1] + 0.5E-5),
        fontproperties={'family': 'serif', 'size': 16, 'weight': 'regular'}
    )


fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.set_xlabel("Field (mT)", fontdict)
ax.set_ylabel('m" (emu)', fontdict)
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

    
# ax.legend(prop=legend_font)

ax.set_title(title, fontdict)

plt.xlim(-10/10, 1100/10)
plt.ylim(df['m" (emu)'].min()-((df['m" (emu)'].min())/50), df['m" (emu)'].max()+((df['m" (emu)'].min())/20))
plt.grid(True)

# plt.savefig(title + '.ACFitHigh.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title + '.ACFitHigh.png', format='png', bbox_inches='tight')

plt.show()



