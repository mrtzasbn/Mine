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

def extract_chunks(df):
    # Define the number of rows in each chunk
    chunk_size = 3
    
    # Create a dictionary to store data for each chunk
    chunk_data = {}
    
    # Iterate over each column
    for col in df.columns:
        # Extract data for each chunk
        chunks = [df[col][i::chunk_size] for i in range(chunk_size)]
        
        # Create a DataFrame for each chunk
        for i, chunk in enumerate(chunks):
            if i not in chunk_data:
                chunk_data[i] = pd.DataFrame()
            chunk_data[i][col] = chunk.values
    
    # Convert dictionary values to list of DataFrames
    return list(chunk_data.values())

# List of file paths and legend labels
file = r"D:\MyData\CERN\R192-5\SQUID\AC-5K_Field_R192-5_High.ac.dat"
title= "Nb$_3$Sn Thin Film, Sample 192-5, High Field"

df = read_squid_data(file).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit"]]

dfs = extract_chunks(df)
# Plotting
fig, ax = plt.subplots(figsize=(10, 8))

for i, df_chunk in enumerate(dfs):
    df_chunk = df_chunk[df_chunk["Regression Fit"] > 9.99E-1]
    ax.plot(df_chunk['Field (Oe)'] / 10, df_chunk['m" (emu)'], label=f"data {i+1}", marker="o")

# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_xlabel("Field (mT)", fontdict)
ax.set_ylabel('m" (emu)', fontdict)

ax.set_title(title, fontdict)

ax.legend(prop=legend_font)
# Set tick labels
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

ax.grid(True)

plt.tight_layout()
plt.show()
