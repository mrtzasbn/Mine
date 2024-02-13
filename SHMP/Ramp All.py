import pandas as pd
import matplotlib.pyplot as plt


def hall_data(file):
    hall_data = pd.read_csv(
        file, delim_whitespace=True, comment='#', header=None,
        names=['time(s)', 'Hall_Voltage(V)', 'Field(T)']
    )
    return hall_data

def ramp(file, hall_constant_value):
    data = hall_data(file)
    offset = data['Hall_Voltage(V)'].iloc[0]
    data['Hall_Voltage(V)'] = (data['Hall_Voltage(V)'] - offset) * hall_constant_value
    return data

# Provide the file path
file2090 = r'D:\R192-5\Ramp\hc1_ramp2090.dat'
file2095 = r'D:\R192-5\Ramp\hc1_ramp2095.dat'
file2100 = r'D:\R192-5\Ramp\hc1_ramp2100.dat'

title = "Ramp up to 100 mT"

# title = "Ramp for 2090"
ramp2090 = ramp(file2090, 46.12)
ramp2095 = ramp(file2095, 47.75)
ramp2100 = ramp(file2100, 46.46)

fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(ramp2090['Field(T)']*1000, ramp2090['Hall_Voltage(V)']*1000, label="2090")
ax.scatter(ramp2095['Field(T)']*1000, ramp2095['Hall_Voltage(V)']*1000, label="2095")
ax.scatter(ramp2100['Field(T)']*1000, ramp2100['Hall_Voltage(V)']*1000, label="2100")

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

ax.set_xlabel("Applied Field (mT)", fontdict)
ax.set_ylabel('Measured Field (mT)', fontdict)
ax.set_title(title, fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)
ax.legend(prop=legend_font)

plt.grid(True)

plt.savefig(title+'.pdf', format='pdf', bbox_inches='tight')
plt.savefig(title+'.png', format='png', bbox_inches='tight')
plt.show()
