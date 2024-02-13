import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Define a function for the linear model
def linear(x, a, b):
    return a * x + b

file = r"D:\MyData\CERN\R168-5\Hc2_T.csv"
df = pd.read_csv(file)

# title = "T$_c$ vs Field, R168-5, Intersection of Fitting"
title = "T$_c$ vs Field, R168-5,  First deviation from Linear in Dissipation"
interval = [(9.5, 15.5)]


for start, end in interval:
# Mask the data based on the interval
    masked_data = df[(df["T"] >= start) & (df["T"] <= end)]

    x_interval = masked_data["T"]
    y_interval = masked_data["Field"]

    params, _ = curve_fit(linear, x_interval, y_interval)

slope = params[0]
H_intercept = params[1]
T_intercept = -H_intercept/slope

print(f"slope is {slope}")
print(f"Hc2(0)-fitted is {H_intercept}")
print(f"Tc(0)-fitted is {T_intercept}")

fig, ax = plt.subplots(figsize=(10, 8))

# Plotting
ax.scatter(
    df["T"], df["Field"], marker="o", color="black", s=25
    # label="1 T"
            )
# Plotting T intercept ###############################
ax.scatter(T_intercept, 0, color="red", s=50, zorder=3)

ax.annotate(
        f'T$_{{\mathrm{{intercept}}}}$: ({T_intercept:.2f} K)',
            xy=(T_intercept, 0),
            xytext=(T_intercept-5, 0),
            arrowprops=dict(facecolor='black', shrink=0.05),
            fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
    )

# Plotting H intercept ###############################
ax.scatter(0, H_intercept, color="blue", s=50, zorder=3)

ax.annotate(
        f'H$_{{\mathrm{{c2}}}}$(0): ({H_intercept:.2f} T)',
            xy=(0, H_intercept),
            xytext=(0+2, H_intercept),
            arrowprops=dict(facecolor='black', shrink=0.05),
            fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
    )
# Plotting H of WHH ###############################
h_Whh = -0.693*slope*T_intercept
ax.scatter(0, h_Whh, color="green", zorder=3)
ax.annotate(
        f'H$_{{\mathrm{{WHH}}}}$(0): ({h_Whh:.2f} T)',
            xy=(0, h_Whh),
            xytext=(0, h_Whh-3),
            arrowprops=dict(facecolor='black', shrink=0.05),
            fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
    )

# Plot the fitted lines for each interval ###############################
for start, end in interval:
    x_data = np.linspace(0-0.5, end+1, 100)
    y_fit = linear(x_data, slope, H_intercept)
    ax.plot(x_data, y_fit, linestyle="--", linewidth=2)

# Calculate midpoint of x and y data
x_midpoint = np.mean(df["T"])
y_midpoint = np.mean(df["Field"])
ax.annotate(f'Slope: {slope:.2f} T/K', xy=(x_midpoint, y_midpoint), xytext=(x_midpoint , y_midpoint + 2),
            arrowprops=dict(facecolor='green', shrink=0.05),
            fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'})

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.set_xlabel("Temperature (K)", fontdict)
ax.set_ylabel("Field (T)", fontdict)
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

####################################

####################################

# ax.legend(prop=legend_font)
ax.set_title(title, fontdict)

# plt.xlim(-0.5, 18)
# plt.ylim(-0.5, 25)
plt.grid(True)

plt.savefig(title + '.TcDet.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title + '.TcDet.png', format='png', bbox_inches='tight')

plt.show()
