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

def tc_data(file_path):
    tc = read_squid_data(file_path).loc[:, ["Temperature (K)", "m' (emu)", 'm" (emu)']]
    return tc


file = [
    (r"D:\MyData\CERN\R86-5\Tc_1T.ac.dat", "1 T", 'o'),
    (r"D:\MyData\CERN\R86-5\Tc_2T.ac.dat", "2 T", 's'),
    (r"D:\MyData\CERN\R86-5\Tc_3T.ac.dat", "3 T", '^'),
    (r"D:\MyData\CERN\R86-5\Tc_4T.ac.dat", "4 T", 'D'),
    (r"D:\MyData\CERN\R86-5\Tc_5T.ac.dat", "5 T", 'v'),
    (r"D:\MyData\CERN\R86-5\Tc_6T.ac.dat", "6 T", '*'),
    (r"D:\MyData\CERN\R86-5\Tc_7T.ac.dat", "7 T", 'x')
]

title = "T$_c$ of Nb$_3$Sn Thin Film, Sample R94-4"

fig, ax = plt.subplots(figsize=(10, 8))

for file_name, label, marker in file:
    tc = tc_data(file_name)
    ax.plot(tc["Temperature (K)"], tc["m' (emu)"], marker=marker, label=label)

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_xlabel("Temperature (K)", fontdict)
ax.set_ylabel('m" (emu)', fontdict)
ax.set_title(title, fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

plt.grid(True)
plt.legend(prop=legend_font)
plt.tight_layout()

# plt.savefig(title + '.TcAppFieldDis.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(title + '.TcAppFieldDis.png', format='png', bbox_inches='tight')

plt.show()
