import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker


file_path = r"F:\OffsetData.dat"
file_encoding = 'utf-8'  # Adjust the encoding if needed

# Read the data from the file into a DataFrame, skipping lines that start with #
df = pd.read_csv(file_path, delim_whitespace=True, comment='#', header=None, names=[
    'time(s)', 'field(T)', 'V_hall(V)', 'V_dms(V)', 'temp(K)', 'temp_VTI(K)', 
    'heater_setpoint(K)', 'heater_power(%)', 'heater_range(id)', 'He(%)', 'x(µm)', 'y(µm)', 'z(µm)'
], encoding=file_encoding)

df['time(s)'] = df['time(s)']-1699007156.426
df = df[(df['time(s)'] >= 5) & (df['time(s)'] <=1520)]
# print(df)
########################
midpoints = []
mean_V_values = []
fields = []

for i in range(0, 101):
    mid = 13 + 15 * i
    midpoints.append(mid)

x1 = np.linspace(0, 0.49, 50)
x2 = np.linspace(0.5, 0, 51)

for i in x1:
    i = round(i, 2)
    fields.append(i)
for i in x2:
    i = round(i, 2)
    fields.append(i)


for midpoint in midpoints:
    # Define the intervals
    intervals = [(midpoint - 3, midpoint + 3)]

    for start, end in intervals:
        # Filter the DataFrame for data within the current interval
        masked_data = df[(df['time(s)'] >= start) & (df['time(s)'] <= end)]
        
        # Calculate the mean of 'V_hall(V)' for the current interval
        mean_V = masked_data['V_hall(V)'].mean()
        # Append the mean value to the list
        mean_V_values.append(mean_V)

print(len(midpoints))
print(len(mean_V_values))
print(len(fields))

# Create a DataFrame
df_new = pd.DataFrame({
    "Time": midpoints,
    "Hall Voltage": mean_V_values,
    "Field": fields
})

delta = df_new.groupby("Field")["Hall Voltage"].apply(lambda x: (x.iloc[0] - x.iloc[1])
                                if len(x) > 1 else None).reset_index().rename(columns={"Hall Voltage": "Delta"})
delta = delta.sort_values("Field")
print(delta)
# ############################
fig, ax = plt.subplots(figsize=(10, 8))


plt.scatter(delta['Field'], delta['Delta'])

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

# Set axis labels
ax.set_xlabel('Field (T)', fontdict)
ax.set_ylabel('\u0394Hall Voltage (V)', fontdict)

plt.title("Hall Voltage difference between changing field [0, 0.5] and back", fontdict)

# Set tick fonts
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)


plt.grid(True)


plt.show()
