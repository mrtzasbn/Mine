import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to read SQUID data and create a DataFrame
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df


fig, axs = plt.subplots(2, 2, figsize=(10, 8))


file_dir = r"D:\Data\Nb3SnData\R143-5"

file_name_infield = "M(H)_5K_R143-5_infield.ac.dat"
file_name_rem = "M(H)_5K_R143-5_rem.ac.dat"


df_infield = read_squid_data(os.path.join(file_dir, file_name_infield)).loc[:, [
                                                "Time",
                                                "Field (Oe)",
                                                 "m' (emu)",
                                                 'm" (emu)'
                                                 ]]

df_rem  = read_squid_data(os.path.join(file_dir, file_name_rem)).loc[:, [
                                                "Time",
                                                "Field (Oe)",
                                                 "m' (emu)",
                                                 'm" (emu)'
                                                 ]]
axs[0, 0].plot(
            df_infield["Field (Oe)"],
            df_infield["m' (emu)"],
            linewidth=2,
            marker="o",
            label=file_name_infield
        )
axs[0, 1].plot(
            df_infield["Field (Oe)"],
            df_infield['m" (emu)'],
            linewidth=2,
            marker="o",
            label=file_name_infield
        )
axs[1, 0].plot(
            df_infield["Field (Oe)"],
            df_rem["m' (emu)"],
            linewidth=2,
            marker="o",
            label=file_name_rem
        )
axs[1, 1].plot(
            df_infield["Field (Oe)"],
            df_rem['m" (emu)'],
            linewidth=2,
            marker="o",
            label=file_name_rem
        )
        

fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}

axs[0, 0].set_xlabel(
                "Field (Oe)",
                  fontdict)
axs[0, 0].set_ylabel(
                    "m' (emu)",
                    fontdict)

axs[0, 1].set_xlabel(
                "Field (Oe)",
                  fontdict)
axs[0, 1].set_ylabel(
                    'm" (emu)',
                    fontdict)
axs[1, 0].set_xlabel(
                "Field (Oe)",
                  fontdict)
axs[1, 0].set_ylabel(
                    "m' (emu)",
                    fontdict)

axs[1, 1].set_xlabel(
                "Field (Oe)",
                  fontdict)
axs[1, 1].set_ylabel(
                    'm" (emu)',
                    fontdict)


axs[0, 0].set_title(f"{file_name_infield}")
axs[0, 1].set_title(f"{file_name_infield}")
axs[1, 0].set_title(f"{file_name_rem}")
axs[1, 1].set_title(f"{file_name_rem}")
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}



# jpg_filename = f"R152-5.jpg"
# plt.savefig(jpg_filename, format="jpg", dpi=300)  # You can adjust the dpi (dots per inch) as needed

plt.tight_layout()
plt.show()
