import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv(r"D:\RawDataSquid\Nb3Sn\81-5\Tc\Tc0.csv")

fig, ax = plt.subplots()

ax.scatter(
            df["Temperature Onset"],
            df["Field"],
            s=75,
            color="black"
        )

slope, intercept, r_value, p_value, std_err = stats.linregress(df["Temperature Onset"], df["Field"])

# Calculate predicted values
predicted_Y = slope * df["Temperature Onset"] + intercept
plt.plot(df["Temperature Onset"], predicted_Y, color='red', label='Linear Fit')

ax.annotate(
        f'Slope: {slope:.2f} T/K\nIntercept: {intercept:.2f} T',
        xy=(12, 6),
        # xytext=(max_field + 0.5, max_jc + 2e6),
        fontproperties={'family': 'serif', 'size': 12, 'weight': 'regular'}
    )

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.set_xlabel("Temperature (K)", fontdict)
ax.set_ylabel("Field (T)", fontdict)
ax.set_title("T$_c$ vs. Magnetic Field", fontdict)


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


# jpg_filename = "TcvsField_squid_plot.jpg"
# plt.savefig(jpg_filename, format="jpg", dpi=300)  # You can adjust the dpi (dots per inch) as needed

plt.show()

print(0.693*15.29*slope)