import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_with_fwhm(x, y):
    # Find the maximum value and its index
    max_index = np.argmax(y)
    max_value = y[max_index]

    # Find the indices where the value drops to half of the maximum
    half_max_value = max_value / 2
    left_index = np.where(y[:max_index] < half_max_value)[0][-1]
    right_index = np.where(y[max_index:] < half_max_value)[0][0] + max_index

    # Calculate the FWHM
    fwhm = x[right_index] - x[left_index]

    # Plot the data
    plt.figure(figsize=(10, 8))
    plt.plot(x, y, label='Data', color="black", marker="o")

    # Plot the peak
    plt.plot(x[max_index], max_value, 'ro', label='Peak')

    # Plot the FWHM points
    plt.plot([x[left_index], x[right_index]], [half_max_value, half_max_value], 'go', label='FWHM points')

    # Annotate FWHM value
    plt.text(x[max_index]+0.5, half_max_value, f'FWHM = {fwhm:.2f}', verticalalignment='bottom', fontdict={'family': 'serif', 'size': 12})

    # Add arrow between FWHM points with custom arrow properties
    plt.annotate('', xy=(x[right_index], half_max_value), xytext=(x[left_index], half_max_value),
                 arrowprops=dict(arrowstyle='<->', color='blue', mutation_scale=15, linewidth=2))

    fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
    legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
    tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

    plt.xlabel("Temperature (K)", fontdict)
    plt.ylabel("m' (emu)", fontdict)
    plt.title('FWHM Calculation', fontdict)
    plt.legend(prop=legend_font, loc='upper left')
    plt.xticks(fontproperties=tick_font)
    plt.yticks(fontproperties=tick_font)
    plt.grid(True)

    # plt.savefig(title + '..pdf', format='pdf', bbox_inches='tight')
    # plt.savefig(title + '..png', format='png', bbox_inches='tight')
    
    plt.show()

# Function to read SQUID data and create a DataFrame
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df


file = r"D:\MyData\CERN\R173-5\SQUID\Tc_0T.ac.dat"

df = read_squid_data(file).loc[:, ["Temperature (K)", "m' (emu)", 'm" (emu)', "m' Scan Std Dev", 'm" Scan Std Dev']]
df = df[(df['m" Scan Std Dev']<9.99E-7) & (df["m' Scan Std Dev"]<9.99E-7)]
df = df[(df["Temperature (K)"]>14)]

title = "FWHM, Nb$_3$Sn Thin Film, Sample 183-5"

x = df["Temperature (K)"].values
y = df['m" (emu)'].values

plot_with_fwhm(x, y)
