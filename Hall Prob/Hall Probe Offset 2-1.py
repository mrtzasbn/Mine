import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker


file_path = r"F:\offset5K.dat"
file_encoding = 'utf-8'  # Adjust the encoding if needed

# Read the data from the file into a DataFrame, skipping lines that start with #
# df = pd.read_csv(file_path, delim_whitespace=True, comment='#', header=None, names=[
#     'time(s)', 'field(T)', 'V_hall(V)', 'V_dms(V)', 'temp(K)', 'temp_VTI(K)', 
#     'heater_setpoint(K)', 'heater_power(%)', 'heater_range(id)', 'He(%)', 'x(µm)', 'y(µm)', 'z(µm)'
# ], encoding=file_encoding)

df = pd.read_csv(
                file_path, delim_whitespace=True, comment='#', header=None,
                names=['time(s)', 'Hall_Voltage(V)', 'Field(T)']
                 )
# df['time(s)'] = df['time(s)']-1699007156.426
df = df[(df['time(s)'] >= 0) & (df['time(s)'] <= 2*1676)]

########################
midpoints = []
mean_V_values = []
fields = []

for i in range(0, 101):
    mid = 15 + 15 * i
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

    # Create an empty list to store the mean values for each interval
    

    for start, end in intervals:
        # Filter the DataFrame for data within the current interval
        masked_data = df[(df['time(s)'] >= start) & (df['time(s)'] <= end)]
        
        # Calculate the mean of 'V_hall(V)' for the current interval
        mean_V = masked_data['Hall_Voltage(V)'].mean()
        # Append the mean value to the list
        mean_V_values.append(mean_V)

############################
df_new = pd.DataFrame({
    "Time": midpoints,
    "Hall Voltage": mean_V_values,
    "Field": fields
})


fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(df['time(s)'], df['Hall_Voltage(V)'])
ax.scatter(midpoints, mean_V_values, s=10, color = "red")

# # for i in midpoints:    
# #     plt.axvline(x=i, color='green', linestyle='--')
# # Set font properties
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

# Set axis labels
ax.set_xlabel('time(s)', fontdict)
ax.set_ylabel('Hall Voltage (V)', fontdict)

plt.title("Hall Voltage between changing field [0.5, -0.5] and back", fontdict)

# Set tick fonts
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

plt.grid(True)


plt.show()

