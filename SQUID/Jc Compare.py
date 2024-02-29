import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = [
    (r"D:\MyData\Codes\Mine\JcDataR192-5.csv", "R192-5, Interlayer: Ta, Stiochiometric"),
    (r"D:\MyData\Codes\Mine\JcDataR183-5.csv", "R183-5, Interlayer: None, Stiochiometric"),
    (r"D:\MyData\Codes\Mine\JcDataR173-5.csv", "R173-5, Interlayer: Nb, 27%Sn"),
    (r"D:\MyData\Codes\Mine\JcDataR168-5.csv", "R168-5, Interlayer: Ta, 27%Sn"),
    # (r"D:\MyData\CERN\R94-4\SQUID\JcData.csv", "R94-4, Interlayer: Ta, Stiochiometric")
]

title = "Jc"

fig, ax = plt.subplots(figsize=(10, 8))

for file, label in files:
    df = pd.read_csv(file)
    max = df['Jc'].max()
    # Scatter plot
    ax.scatter(df["Field (Oe)"]*1E-4, df["Jc"], s=25, label=label)

# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
ax.set_xlabel("Applied Field (T)", fontdict)
ax.set_ylabel("J$_c^G$ ($\\times 10^{{{:d}}}$ A/m$^2$)".format(10), fontdict)  # Adjust this label as needed
# ax.set_ylabel("J$_c^G$ (Normalized)", fontdict)  # Adjust this label as needed

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
