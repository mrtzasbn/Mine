import pandas as pd
import matplotlib.pyplot as plt


######### Reading SQUID Data  and Creating a DataFrame #########
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break

    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    # print(squid_data_df)
    return squid_data_df


df = pd.read_csv(r"D:\Data\D\TiR\TiR-1\S30\TiR-1_2018-09-24.rso for 15 K.dat").loc[:, ['Field (Oe)', 'Long Moment (emu)']]

num_indices = df.shape[0]

# Dividing DataSet into F-M-M
first_col = df['Field (Oe)'][:int(num_indices / 2)]
second_col = df['Long Moment (emu)'][:int(num_indices / 2)]
third_col = df['Long Moment (emu)'][int(num_indices / 2):][::-1].reset_index(drop=True)
df_new = pd.DataFrame({
    'Field': first_col,
    'M+': second_col,
    'M-': third_col,
})


# Define the interval for the x-axis (Field values)
interval_start = 0
interval_end = 68000

# Mask the data based on the interval
masked_data = df_new[(df_new['Field'] >= interval_start) & (df_new['Field'] <= interval_end)]

# Plotting M+ and abs(M-) vs Field within the specified interval
plt.scatter(masked_data['Field'], masked_data['M+'], label='M+')
plt.scatter(masked_data['Field'], masked_data['M-'], label='|M-|')

# Adding labels and title
plt.xlabel('Field (Oe)')
plt.ylabel('Magnetic Moment (emu)')
plt.title('M+ and |M-| vs Field (Interval: {} to {})'.format(interval_start, interval_end))

# Adding a legend
plt.legend()

# Display the plot
plt.show()