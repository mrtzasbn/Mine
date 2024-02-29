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
file = r"D:\MyData\CERN\R94-4\SQUID\AC-5K_Field_R94-5_High.ac.dat"
title= "Sample 94-4"

df = read_squid_data(file).loc[:, ['Field (Oe)', "m' (emu)", 'm" (emu)', "Regression Fit"]]

# str = "m' (emu)"
str = 'm" (emu)'
dfs = extract_chunks(df)


df1 = dfs[0]
df2 = dfs[1]
df3 = dfs[2]

fig, ax = plt.subplots(figsize=(10, 8))

for i, df_chunk in enumerate(dfs):
    df_chunk = df_chunk[df_chunk["Regression Fit"] > 9.99E-1]
    ax.plot(df_chunk['Field (Oe)']/10, df_chunk[str], label=f"ac {i+1}", marker="o")

# ax.plot(df1["Field (Oe)"]/10, df1[str]-df2[str], label="ac 1 - ac 2")
# ax.plot(df1["Field (Oe)"]/10, df1[str]-df3[str], label = "ac 1 - ac 3")
# ax.plot(df1["Field (Oe)"]/10, df2[str]-df3[str], label = "ac 2 - ac 3")
f = 500
print((df1.loc[df1["Field (Oe)"] == f, str].values[0])-(df2.loc[df2["Field (Oe)"] == f, str].values[0]))
print((df1.loc[df1["Field (Oe)"] == f, str].values[0])-(df3.loc[df3["Field (Oe)"] == f, str].values[0]))
print((df2.loc[df2["Field (Oe)"] == f, str].values[0])-(df3.loc[df3["Field (Oe)"] == f, str].values[0]))


# Set labels and title
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_xlabel("Applied Field (mT)", fontdict)
ax.set_ylabel(str, fontdict)

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
# plt.savefig(title + '.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title + '.png', format='png', bbox_inches='tight')
# plt.show()
