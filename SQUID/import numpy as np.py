import numpy as np
import pandas as pd
from scipy import interpolate

def calculate_fwhm(x, y, interp_methods=['linear', 'cubic', 'quadratic', 'akima']):
    fwhm_values = {}  # Dictionary to store FWHM values for each method
    
    # FWHM for original data without interpolation
    max_index = np.argmax(y)
    max_value = y[max_index]
    half_max_value = max_value / 2
    left_index = np.where(y[:max_index] < half_max_value)[0][-1]
    right_index = np.where(y[max_index:] < half_max_value)[0][0] + max_index
    fwhm_values['original'] = x[right_index] - x[left_index]
    
    # Interpolation methods
    for method in interp_methods:
        if method == 'akima':
            f = interpolate.Akima1DInterpolator(x, y)
            x_interp = np.linspace(min(x), max(x), 1000)
            y_interp = f(x_interp)
        else:
            f = interpolate.interp1d(x, y, kind=method)
            x_interp = np.linspace(min(x), max(x), 1000)
            y_interp = f(x_interp)
        
        # Find the maximum value and its index
        max_index = np.argmax(y_interp)
        max_value = y_interp[max_index]

        # Find the indices where the value drops to half of the maximum
        half_max_value = max_value / 2
        left_index = np.where(y_interp[:max_index] < half_max_value)[0][-1]
        right_index = np.where(y_interp[max_index:] < half_max_value)[0][0] + max_index

        # Calculate the FWHM
        fwhm_values[method] = x_interp[right_index] - x_interp[left_index]
        
    return fwhm_values


# Function to read SQUID data and create a DataFrame
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df


file = r"D:\MyData\CERN\R183-5\SQUID\Tc_0T.ac.dat"

df = read_squid_data(file).loc[:, ["Temperature (K)", "m' (emu)", 'm" (emu)', "m' Scan Std Dev", 'm" Scan Std Dev']]
df = df[(df['m" Scan Std Dev'] < 9.99E-7) & (df["m' Scan Std Dev"] < 9.99E-7)]
df = df[(df["Temperature (K)"] > 14)]

x = df["Temperature (K)"].values
y = df['m" (emu)'].values

fwhm_values = calculate_fwhm(x, y, interp_methods=['linear', 'cubic', 'quadratic', 'akima'])

# Print FWHM values
print("FWHM Values:")
for method, fwhm in fwhm_values.items():
    print(f"{method.capitalize()} Interpolation: {fwhm:.2f}")
