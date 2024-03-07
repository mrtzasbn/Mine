import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define a function for the linear model
def linear(x, a, b):
    return a * x + b


file = r"D:\MyData\CERN\R192-5\SQUID\Hc2_T.csv"

# title = "R173-5, Intersection of Fitting"
# title = "R86-5, First deviation from Linear in Dissipation"
title = "\u03BC$_0$H$_c$$_2$ vs T, R192-5"

fig, ax = plt.subplots(figsize=(10, 8))


df = pd.read_csv(file)
tc = df["T"].iloc[0]
print(tc)
df = df.drop(index=0).reset_index(drop=True)

start, end = (df["T"].iloc[-1], df["T"].iloc[0])
masked_data = df[(df["T"] >= start) & (df["T"] <= end)]

x_interval = masked_data["T"]
y_interval = masked_data["Field"]
params, _ = curve_fit(linear, x_interval, y_interval)

slope = params[0]
H_intercept = params[1]
T_intercept = -H_intercept/slope


# Fitting
x_data = np.linspace(start-1, end+1, 100)
y_fit = linear(x_data, slope, H_intercept)
    

# WHH
h_Whh = -0.693*slope*T_intercept


new_data = {'T': [0, T_intercept], 'Field': [h_Whh, 0]}
new_df = pd.DataFrame(new_data)
df = pd.concat([df, new_df], ignore_index=True)
df = df.sort_values(by='T')

# Main Data
ax.scatter(df["T"], df["Field"], marker="o", color="black", s=25)
# Plot the fit ###############################
ax.plot(x_data, y_fit, linestyle="--", linewidth=2)

# # Plotting T intercept ###############################
# ax.scatter(T_intercept, 0, color="red", s=50, zorder=3) 
# ax.annotate(
#         f'T$_{{\mathrm{{intercept}}}}$: ({T_intercept:.2f} K)',
#             xy=(T_intercept, 0),
#             xytext=(T_intercept-5, 0),
#             arrowprops=dict(facecolor='black', shrink=0.05),
#             fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
#     )
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

# Calculate midpoint of x and y data
x_midpoint = np.mean(df["T"])
y_midpoint = np.mean(df["Field"])
ax.annotate(f'Slope: {slope:.2f} T/K', xy=(x_midpoint, y_midpoint), xytext=(x_midpoint , y_midpoint + 3),
            # arrowprops=dict(facecolor='green', shrink=0.05),
            fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'})

    


fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 10, 'weight': 'regular'}
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}


ax.set_xlabel("T (K)", fontdict)

ax.set_ylabel("\u03BC$_0$H$_c$$_2$ (T)", fontdict)
ax.set_title(title, fontdict)
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

# ax.legend(prop=legend_font)
plt.grid(True)

# Saving the plot
# plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title+'.png', format='png', bbox_inches='tight')
plt.show()
