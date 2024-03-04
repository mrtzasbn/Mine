import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.ticker as ticker

# Define a function for the linear model
def linear(x, a, b):
    return a * x + b


# List of 8 main colors
main_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange']

files = [
    (r"D:\MyData\CERN\R86-5\Hc2_T.csv", "R192-5, Interlayer: Ta, Stiochiometric"),
    # (r"D:\MyData\CERN\R183-5\SQUID\Hc2_T.csv", "R183-5, Interlayer: None, Stiochiometric"),
    # (r"D:\MyData\CERN\R173-5\SQUID\Hc2_T.csv", "R173-5, Interlayer: Nb, 27%Sn"),
    # (r"D:\MyData\CERN\R168-5\SQUID\Hc2_T.csv", "R168-5, Interlayer: Ta, 27%Sn"),
    # (r"D:\MyData\CERN\R94-4\SQUID\Hc2_T.csv", "R94-4, Interlayer: Ta, Stiochiometric")
]

title = "Temperature vs. Field"
fig, ax = plt.subplots(figsize=(10, 8))

for i, (file, label) in enumerate(files):
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

    color = main_colors[i % len(main_colors)]  # Cycle through main colors

    # Fitting
    x_data = np.linspace(start-1, end+1, 100)
    y_fit = linear(x_data, slope, H_intercept)
    
    # Plot the fit
    ax.plot(x_data/T_intercept, y_fit, linestyle="-", linewidth=2, color=color)

    # WHH
    h_Whh = -0.693*slope*T_intercept


    new_data = {'T': [0, T_intercept], 'Field': [h_Whh, 0]}
    new_df = pd.DataFrame(new_data)
    df = pd.concat([df, new_df], ignore_index=True)
    df = df.sort_values(by='T')

    # Main Data
    ax.scatter(df["T"]/T_intercept, df["Field"], s=50,
               label=f"{label},\nSlope: {slope:.2f}, T$_c$(0): {tc}K, H$_{{\mathrm{{WHH}}}}$(0): ({h_Whh:.2f} T)\n---------------------------------", color=color)
    



    


fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 10, 'weight': 'regular'}
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}


ax.set_xlabel("T/T$_c$", fontdict)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.set_ylabel("\u03BC$_0$H$_c$$_2$ (T)", fontdict)

for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

ax.legend(prop=legend_font)
plt.grid(True)

# Saving the plot
# plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title+'.png', format='png', bbox_inches='tight')
plt.show()
