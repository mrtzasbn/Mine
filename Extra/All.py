import pandas as pd
import matplotlib.pyplot as plt
import os
##################################################################################
# Reading Data From SQUID file
def read_squid_data(filename):
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if "[Data]" in line:
                skiprows = i + 1
                break
    squid_data_df = pd.read_csv(filename, skiprows=skiprows)
    return squid_data_df
##################################################################################
# Plotting Magnetization
def plot_magnetization_squid(data_dir, data_info, interval_start, interval_end):
    fig, ax = plt.subplots()

    for file_name, legend_label in data_info:
        file_path = os.path.join(data_dir, file_name)
        df = read_squid_data(file_path).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
        masked_data = df[(df['Field (Oe)'] >= interval_start) & (df['Field (Oe)'] <= interval_end)]
        ax.plot(
            masked_data['Field (Oe)'] / 10000,
            masked_data['Long Moment (emu)'],
            linewidth=2,
            label=legend_label
        )

    customize_plot(ax, "Field (T)", "Long Moment (emu)", "Long Moment")
##################################################################################
# Plotting Susceptibility data
def plot_susceptibility_squid(data_dir, data_info):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    
    for file_name, legend_label in data_info:
        file_path = os.path.join(data_dir, file_name)
        df = read_squid_data(file_path).loc[:, ["Temperature (K)", "m' (emu)", 'm" (emu)']]
        ax1.scatter(
            df["Temperature (K)"],
            df["m' (emu)"],
            # linewidth=2,
            label=legend_label
        )
        ax2.plot(
            df["Temperature (K)"],
            df['m" (emu)'],
            linewidth=2,
            label=legend_label
        )
    fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
    legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
    ax1.set_ylabel("m' (emu)", fontdict)
    ax1.set_title("Susceptibility", fontdict)

    tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
    for tick in ax1.get_xticklabels():
        tick.set(**tick_font)
    for tick in ax1.get_yticklabels():
        tick.set(**tick_font)
    ax1.legend(prop=legend_font)
    fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
    ax2.set_xlabel("Temperature (K)", fontdict)
    ax2.set_ylabel('m" (emu)', fontdict)
    tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
    for tick in ax2.get_xticklabels():
        tick.set(**tick_font)
    for tick in ax2.get_yticklabels():
        tick.set(**tick_font)
    ax2.legend(prop=legend_font)
    plt.show()
##################################################################################
# Plotting Jc from Magnetization data
def plot_jc_squid(data_dir, data_info, interval_start, interval_end):
    # Input sample dimension
    a = 1860E-6
    b = 1960E-6
    d = 3E-6
    coefficient = 4 / (a**2 * b * d * (1 - (a / (3 * b))))

    fig, ax = plt.subplots(data_dir, data_info)

    for file_name, legend_label in data_info:
        file_path = os.path.join(data_dir, file_name)
        df = read_squid_data(file_path).loc[:, ['Field (Oe)', 'Long Moment (emu)']]
        num_indices = df.shape[0]

        first_col = df['Field (Oe)'][:int(num_indices / 2)]
        second_col = df['Long Moment (emu)'][:int(num_indices / 2)]
        third_col = df['Long Moment (emu)'][int(num_indices / 2):][::-1].reset_index(drop=True)

        df_new = pd.DataFrame(
            {
                'Field': first_col,
                'M+': second_col,
                'M-': third_col
            }
        )

        df_new["Jc"] = 1E-3 * coefficient * abs((df_new["M+"] - df_new["M-"])) / 2
        masked_data = df_new[
            (df_new['Field'] >= interval_start)
            & (df_new['Field'] <= interval_end)
                            ]

        ax.plot(
            masked_data['Field'] / 10000,
            masked_data['Jc'],
            linewidth=3,
            label=legend_label
        )

    customize_plot(ax, "Field (T)", "J$_c$ (A/m$^2$)", "J$_c$")
##################################################################################

def customize_plot(ax, xlabel, ylabel, title):
    fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
    ax.set_xlabel(xlabel, fontdict)
    ax.set_ylabel(ylabel, fontdict)
    ax.set_title(title, fontdict)

    tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
    for tick in ax.get_xticklabels():
        tick.set(**tick_font)
    for tick in ax.get_yticklabels():
        tick.set(**tick_font)

    legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
    ax.legend(prop=legend_font)
    plt.grid(True)
    plt.show()
##################################################################################

if __name__ == "__main__":
# Data directory
    data_dir = r"D:\RawDataSquid\Nb3Sn\Wire\TiR"

# List of file paths and legend labels
    data_info = [
    ("TiR-1_2018-09-24_Tc.ac.dat", "Old Measurement"),
    ("TiR-1_2018-09-24_Tc.acNM.dat", "New Measurement"),
    # ("M(T)_1T_AC_zfc_2.ac.dat", "1 T"),
    # ("M(T)_3T_AC_zfc_2.ac.dat", "3 T"),
    # ("M(T)_5T_AC_zfc_2.ac.dat", "5 T"),
    # ("M(T)_7T_AC_zfc_2.ac.dat", "7 T")
]

    plot_susceptibility_squid(data_dir, data_info)
