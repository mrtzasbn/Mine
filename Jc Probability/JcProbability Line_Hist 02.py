import matplotlib.pyplot as plt
import numpy as np

def matrix_J(file):
    matrix = np.loadtxt(file, comments='#')
    return matrix

def plot_histogram(file, bins=100, power=10):
    file_condition_mapping = {
    "J": {"label": "J$_c^L$", "hist_color": "orange"},
    "x": {"label": "J$_x$", "hist_color": "green"},
    "y": {"label": "J$_y$", "hist_color": "blue"}
                    }
    
    file_suffix = file[-5]
    if file_suffix in file_condition_mapping:
        condition_data = file_condition_mapping[file_suffix]
        label = condition_data["label"]
        hist_color = condition_data["hist_color"]
    else:
        # Handle the case when file[-5] doesn't match any condition
        label = "Unknown Label"
        hist_color = "Unknown Color"

    matrix = matrix_J(file)
    num_rows, num_columns = matrix.shape
    print(f"Number of rows: {num_rows}\nNumber of columns: {num_columns}")

    data_flat = matrix.flatten()

    fig, ax = plt.subplots(figsize=(10, 8))

    normal_value = 1 * 10 ** power
    

    hist_values, bins, _ = plt.hist(data_flat/normal_value, bins=bins, color=hist_color,
                                    edgecolor='white', density=True, alpha=1, label=label)

    bin_width = bins[1] - bins[0]
    ax.plot(bins[:-1] + bin_width / 2, hist_values, color='red', linewidth=2)

    fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}
    ax.set_xlabel('{} ($\\times 10^{{{}}}$ A/m$^2$)'.format(label, power), fontdict)
    ax.set_ylabel('Probability Density', fontdict)

    tick_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
    for tick in ax.get_xticklabels():
        tick.set(**tick_font)
    for tick in ax.get_yticklabels():
        tick.set(**tick_font)

    legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
    ax.legend(prop=legend_font)

    plt.tight_layout()

    # plt.savefig(file[:-4]+'.pdf', format='pdf', bbox_inches='tight')
    # plt.savefig(file[:-4]+'.png', format='png', bbox_inches='tight')

    plt.show()


file_path = r"D:\Nb3Sn ThinFilm\Nb3Sn8105\Nb3Sn8105_J.mat"
plot_histogram(file_path, bins=100, power=10)
