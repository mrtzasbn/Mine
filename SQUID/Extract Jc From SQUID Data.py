import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to read SQUID data and create a DataFrame
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df

def groupby_squid_jc(file_path, coefficient, interval_start, interval_end, exception=70000):
    # Read SQUID data and select relevant columns
    df = read_squid_data(file_path).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
    # df["Field (Oe)"] = -df["Field (Oe)"]
    # df['Long Moment (emu)'] = -df['Long Moment (emu)']
    if exception is None:
        df = df[df["Field (Oe)"]]
    else:
        df = df[df["Field (Oe)"] != exception]
    df = df[(df['Field (Oe)'] >= interval_start) & (df['Field (Oe)'] <= interval_end)]
    grouped_by  = df.groupby("Field (Oe)")
    df_new = grouped_by["Long Moment (emu)"].apply(
            lambda group: 1E-3 * coefficient * (abs((group.min() - group.max())) / 2)
            if len(group) > 1 
            else np.nan
        ).reset_index(name="Jc")
    return df_new



# Data directory
# List of file paths and legend labels
file = r"D:\MyData\CERN\R168-5\SQUID\M(H)_loop_168_5_5K_WholeLoop.dc.dat"
title = "R168-5"

# Input sample dimension


a = 2462E-6
b = 2344E-6  # Smaller Than "a"
d = 3E-6
coefficient = 4 / (b**2 * a * d * (1 - (b / (3 * a))))
# coefficient = 1
# Interval for x-axis (Field values)
interval_start = 0
interval_end = 70000

result_df = groupby_squid_jc(file, coefficient, interval_start, interval_end)

# to_save = file.split('\\')[:-1]
# to_save = "\\".join(to_save)

result_df.to_csv(f"D:\MyCodes\Mine\JcData{title}.csv", index=False)
