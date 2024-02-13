import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(r"D:\Scripts\Presentation\Tc_All_Samples.csv")
print(df)

fig, ax = plt.subplots(figsize=(11, 9))

ax.scatter(
    df["Sample"],
      df["Tc"],
      s=100
      )

ax.scatter(df["Sample"][0],
      df["Tc"][0],
      s=150,
      c="r")
# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax.set_xlabel("Sample", fontdict)
ax.set_ylabel("T$_c$ (K)", fontdict)
ax.set_title("T$_c$ per Sample", fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
    tick.set(rotation=45, ha='right')
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}


# Display the plot
plt.grid(True)

# jpg_filename = "samples_Tc.jpg"
# plt.savefig(jpg_filename, format="jpg", dpi=300)  # You can adjust the dpi (dots per inch) as needed
plt.show()