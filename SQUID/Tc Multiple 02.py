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

def tc_data (file_path):
    tc = read_squid_data(file_name).loc[:, ["Temperature (K)",
                                                 "m' (emu)",
                                                 'm" (emu)'
                                                 ]]
    return tc


file = [
      (r"D:\Data\SQUID Data\Nb3Sn ThinFilm\R81-5\Mag Loop\0 TN0_3Oe - Tc zfc.ac.dat", "New Cut"),
      (r"D:\Data\SQUID Data\Nb3Sn ThinFilm\R81-5\Mag Loop\0 TN0_3OeOldSample - Tc zfc.ac.dat", "Old Cut")
      ]

title = "T$_c$ of Nb$_3$Sn Thin Film, 2 different cuts of Sample 81-5"


fig, ax = plt.subplots(figsize=(10, 8))


tc_list = []
labels = []
for file_name, label in file:
    labels.append(label)
    tc = tc_data(file_name)
    tc_list.append(tc)

print(labels)
ax.scatter(tc_list[0]["Temperature (K)"], -tc_list[0]["m' (emu)"]/tc_list[0]["m' (emu)"].min(), label=labels[0])
ax.scatter(tc_list[1]["Temperature (K)"], -tc_list[1]["m' (emu)"]/tc_list[1]["m' (emu)"].min(), label=labels[1])

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.legend(prop=legend_font)
ax.set_xlabel("Temperature (K)", fontdict)
ax.set_ylabel(
                    "m' (emu) (Normalized)",
                    fontdict)
ax.set_title(title, fontdict)


tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)


plt.grid(True)

plt.tight_layout()
plt.xlim(14, 18)
plt.savefig(title + '.Tc.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title + '.Tc.png', format='png', bbox_inches='tight')

plt.show()
