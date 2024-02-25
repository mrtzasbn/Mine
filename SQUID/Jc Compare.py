import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = [
    (r"D:\Data\CERN\R192-5\SQUID\JcData.csv", "R192-5, Interlayer: Ta, Stiochiometric"),
    (r"D:\Data\CERN\R183-5\SQUID\JcData.csv", "R183-5, Interlayer: None, Stiochiometric"),
    (r"D:\Data\CERN\R173-5\SQUID\JcData.csv", "R173-5, Interlayer: Nb, 27%Sn"),
    (r"D:\Data\CERN\R168-5\SQUID\JcData.csv", "R168-5, Interlayer: Ta, 27%Sn")
]

title = "Jc"

fig, ax = plt.subplots(figsize=(10, 8))

for file, label in files:
    df = pd.read_csv(file)
    
    # Scatter plot
    ax.scatter(df["Field (Oe)"]*1E-4, df["Jc"], s=50, label=label)

# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax.set_xlabel("Field (Oe)", fontdict)
ax.set_ylabel("Jc", fontdict)  # Adjust this label as needed

ax.set_title(title, fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.legend(prop=legend_font)

# Display the plot
plt.grid(True)
plt.tight_layout()

plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title+'.png', format='png', bbox_inches='tight')
plt.show()
