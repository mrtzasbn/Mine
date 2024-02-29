import pandas as pd
import matplotlib.pyplot as plt

# Function to read SQUID data and create a DataFrame
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df



# List of file paths and legend labels
file = r"D:\MyData\CERN\R94-4\SQUID\AC Modified\AC-5K_Field_R94-5_High_Modified01.ac.dat"
title= "Sample 94-4, more AC"

df = read_squid_data(file).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit"]]



grouped = df.groupby("Field (Oe)")

plt.figure()

# Plot 'Value' against index for each group
for name, group in grouped:
    plt.plot(group.reset_index(drop=True)['m" (emu)'], label=f'Field {name} (Oe)', marker = 'o')

plt.title('m" (emu) vs  AC tries for 500 Oe, Field-Cooling')
plt.xlabel('Try')
plt.ylabel('m" (emu)')
plt.legend()
plt.grid(True)
plt.show()




