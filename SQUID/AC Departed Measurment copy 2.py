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
file = r"D:\MyData\CERN\R86-5\AC Modified\80mT\AC-5K_Field_R86-5_High_ModifiedMoreAC1Hz80mT.ac.dat"
file02 = r"D:\MyData\CERN\R86-5\AC Modified\80mT\AC-5K_Field_R86-5_High_ModifiedMoreAC10min80mT.ac.dat"
file03 = r"D:\MyData\CERN\R86-5\AC Modified\80mT\AC-5K_Field_R86-5_High_ModifiedMoreAC80mT.ac.dat"
title= "Sample 86-5"

df = read_squid_data(file).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit", "Time"]]
df2 = read_squid_data(file02).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit", "Time"]]
df3 = read_squid_data(file03).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit", "Time"]]

# str = "m' (emu)"
str = 'm" (emu)'
dfs = extract_chunks(df)



fig, ax = plt.subplots(figsize=(10, 8))

for i, df_chunk in enumerate(dfs):
    df_chunk = df_chunk[df_chunk["Regression Fit"] > 9.999E-1]
    ax.plot(df_chunk['Field (Oe)']/10, df_chunk[str]*1E6, label=f"ac (fr= 0.1 Hz) {i+1}", marker="+")



dfs_w = extract_chunks(df2)
for i, df_chunk in enumerate(dfs_w):
    df_chunk = df_chunk[df_chunk["Regression Fit"] > 9.999E-1]
    ax.plot(df_chunk['Field (Oe)']/10, df_chunk[str]*1E6, label=f"ac (fr= 1 Hz) {i+1}", marker="*")



dfs_w_ = extract_chunks(df3)
for i, df_chunk in enumerate(dfs_w_):
    df_chunk = df_chunk[df_chunk["Regression Fit"] > 9.99E-1]
    ax.scatter(df_chunk['Field (Oe)']/10, df_chunk[str], label=f"ac_fr_w+ {i+1}", marker="o", s=100)
















# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_xlabel("Applied Field (mT)", fontdict)
# ax.set_ylabel(str, fontdict)
ax.set_ylabel('m" $\\times 10^{{{-6}}}$ (emu)', fontdict)

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
# plt.savefig(file.split("\\")[-1] + '1.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(file.split("\\")[-1] + '1.png', format='png', bbox_inches='tight')
# plt.savefig(title + '+com_fr.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title + '+com_fr.png', format='png', bbox_inches='tight')
plt.show()
