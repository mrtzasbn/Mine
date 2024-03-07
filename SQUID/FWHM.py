import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def peak(x, c):
    return np.exp(-np.power(x - c, 2) / 16.0)

def lin_interp(x, y, i, half):
    return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))

def half_max_x(x, y):
    half = max(y) / 2.0
    signs = np.sign(np.add(y, -half))
    zero_crossings = (signs[0:-2] != signs[1:-1])
    zero_crossings_i = np.where(zero_crossings)[0]
    return [lin_interp(x, y, zero_crossings_i[0], half),
            lin_interp(x, y, zero_crossings_i[1], half)]

# Function to read SQUID data and create a DataFrame
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df

file = r"D:\MyData\CERN\R192-5\SQUID\Tc_ZFC.ac.dat"

df = read_squid_data(file).loc[:, ["Temperature (K)", "m' (emu)", 'm" (emu)', "m' Scan Std Dev", 'm" Scan Std Dev']]
df = df[(df['m" Scan Std Dev'] < 9.99E-7) & (df["m' Scan Std Dev"] < 9.99E-7)]
df = df[(df["Temperature (K)"] > 12)]

title = "Nb$_3$Sn Thin Film, R192-5"

x = df["Temperature (K)"].values
y = df['m" (emu)'].values

# find the two crossing points
hmx = half_max_x(x, y)

# calculate FWHM
fwhm = hmx[1] - hmx[0]
print("FWHM: {:.3f}".format(fwhm))


# plot
plt.figure(figsize=(10, 8))

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

plt.plot(x, y, label='Data', color='black', marker="o", linewidth=2)
plt.plot(hmx, [max(y) / 2.0, max(y) / 2.0], label='FWHM line', color='red', linewidth=3)
plt.annotate('FWHM: {:.2f}K'.format(fwhm), xy=(np.mean(hmx), max(y) / 2.0),
             xytext=(np.mean(hmx)+0.5, max(y) / 2.0 + max(y) / 10),
            #  arrowprops=dict(facecolor='red', arrowstyle='->', shrink=0.05),
             arrowprops=dict(facecolor='green', shrink=0.05),
             horizontalalignment='center', verticalalignment='bottom', fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'})



plt.xlabel("Temperature (K)", fontdict)
plt.ylabel("m' (emu)", fontdict)
plt.title('FWHM Calculation, '+title, fontdict)
plt.legend(prop=legend_font, loc='upper left')
plt.xticks(fontproperties=tick_font)
plt.yticks(fontproperties=tick_font)
plt.grid(True)

plt.legend(prop=legend_font)
# plt.savefig('FWHM Calculation ' + title + '.pdf', format='pdf', bbox_inches='tight')
plt.savefig('FWHM Calculation ' + title + '.png', format='png', bbox_inches='tight')

plt.show()
