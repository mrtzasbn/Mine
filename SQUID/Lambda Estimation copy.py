import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math


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
################################################################

# Constants
phi_0 = 2.067833848E-15  # Wb
mu_0  = 1.25663706212E-6
pi_value = math.pi

a = 2802E-6
b = 2428E-6
d = 2.67E-6
v = a * b * d

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
################################################################

# file path
file = r"D:\Data\CERN\R173-5\SQUID\M(H)_loop_173_5_14K_HighFields.dc.dat"
title = "Fitted Magnetization of Nb$_3$Sn for Lambda, Sample 173-5"

file22 = r"D:\Data\CERN\R173-5\SQUID\M(H)_loop_173_5_22K.dc.dat"

# Read SQUID data and select relevant columns
df = read_squid_data(file).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
df = df[(df['Field (Oe)'] >= 0) & (df['Field (Oe)'] <= 70000)]

df22 = read_squid_data(file22).loc[:, ['Field (Oe)', 'Long Moment (emu)']]


# chanck = int(len(df['Field (Oe)'])/4)
# df  = df.iloc[1*chanck+0:2*chanck+2, :]

df['Field (Oe)'] = df['Field (Oe)']
df['Mag'] = df['Long Moment (emu)']




grouped_by  = df.groupby("Field (Oe)")
df = grouped_by["Mag"].apply(
            lambda group: ((group.max() + group.min()) / 2)
            if len(group) > 1 
            else np.nan
        ).reset_index(name="rev")
################################################################
df = pd.merge(df, df22, on='Field (Oe)', how='outer')

df["rev-cu"] = (df['rev']-df['Long Moment (emu)'])/v

df['Field (Oe)'] = np.log(df['Field (Oe)']*1E-4)
################################################################

fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(df['Field (Oe)'], df['rev']/v,
        # linewidth=2,
        color= "black",
        label="Experimental Data"
    )
ax.scatter(df['Field (Oe)'], df['rev-cu'],
        # linewidth=2,
        color= "red",
        label="Experimental Data"
    )
###############################################################

interval = (0.2, 2)
start, end = interval
masked_data = df[(df['Field (Oe)'] >= start) & (df['Field (Oe)'] <= end)]

x_interval = masked_data['Field (Oe)']
y_interval = masked_data['rev-cu']

params, _ = curve_fit(linear, x_interval, y_interval)

x_data =df['Field (Oe)']
y_fit = linear(x_data, params[0], params[1])
ax.plot(x_data, y_fit, label="Fitted Line", linewidth=2, color="red")
print(params)
################################################################

lambda_value = math.sqrt((phi_0)/(8*pi_value*params[0]*mu_0))

# Annotation below the legend
annotation = f'Fitted λ(@5): {lambda_value/1E-9:.2f} nm'
ax.text(0.5, 0.05, annotation, transform=ax.transAxes, ha="center",fontsize=20, fontdict=fontdict)
################################################################

# Customize labels, titles, fonts, and legend
ax.set_xlabel("ln(B)", fontdict)
ax.set_ylabel("Magnetization (A/m)", fontdict)
ax.set_title(title, fontdict)


for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

# ax.legend(prop=legend_font)


plt.grid(True)
plt.tight_layout()

# Saving the plot
# plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title+'.png', format='png', bbox_inches='tight')

# # Display the plot
plt.show()