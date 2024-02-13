import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv(r"D:\RawDataSquid\Nb3Sn\81-5\Tc\Tc0.csv")

fig, ax = plt.subplots()

ax.scatter(
            df["Dleta T"],
            df["Field"],
            s=75,
            color="black"
        )

slope, intercept, r_value, p_value, std_err = stats.linregress(df["Dleta T"], df["Field"])

# Calculate predicted values
predicted_Y = slope * df["Dleta T"] + intercept
plt.plot(df["Dleta T"], predicted_Y, color='red', label='Linear Fit')

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.set_xlabel("$\Delta$T (K)", fontdict)
ax.set_ylabel("Field (T)", fontdict)
ax.set_title("$\Delta$T vs. Magnetic Field", fontdict)

tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

print(f"Slope: {slope}")
print(f"Intercept: {intercept}")

# plt.grid(True)

# jpg_filename = "deltaT_squid_plot.jpg"
# plt.savefig(jpg_filename, format="jpg", dpi=300)  # You can adjust the dpi (dots per inch) as needed

plt.show()