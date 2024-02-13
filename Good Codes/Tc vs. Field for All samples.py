import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"D:\Data\Nb3SnData\TcAll.csv")
print(df)

fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(
            df["R81-5"],
            df["Field"],
            # linewidth=2,
            marker="o",
            label = "R81-5"
)
ax.plot(
            df["R133-5"],
            df["Field"],
            # linewidth=2,
            marker="o",
            label = "R133-5"

)
ax.plot(
            df["R143-5"],
            df["Field"],
            # linewidth=2,
            marker="o",
            label = "R143-5"

)
ax.plot(
            df["R151-5"],
            df["Field"],
            # linewidth=2,
            marker="o",
            label = "R151-5"

)
ax.plot(
            df["R152-5"],
            df["Field"],
            # linewidth=2,
            marker="o",
            label = "R152-5"

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

plt.legend(prop=legend_font)

plt.show()