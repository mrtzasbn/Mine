# import matplotlib.pyplot as plt
# import numpy as np

# file = r"D:\Inversion Data\Nb3Sn\Nb3Sn8105\Nb3Sn8105_J.mat"

# # Importing The Matrix
# matrix = np.loadtxt(file, comments='#')

# # Print the shape
# num_rows, num_columns = matrix.shape
# print(f"Number of rows: {num_rows}\nNumber of columns: {num_columns}")

# # Flatten the matrix to a 1D array
# data_flat = matrix.flatten()

# # Create a figure and axes
# fig, ax = plt.subplots(figsize=(10, 8))

# exponent = 10
# normal_value = 1 * 10 ** exponent


# # Plot the histogram
# ax.hist(data_flat/normal_value, bins=50, color='blue', edgecolor='black', density=True, label="J$_c^L$")

# # Customize labels, titles, fonts, and legend
# fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}

# # Set x-axis label with proper formatting
# ax.set_xlabel('J$_c^L$ ($\\times 10^{{{}}}$ A/m$^2$)'.format(exponent), fontdict)

# # Set y-axis label
# ax.set_ylabel('Probability Density', fontdict)

# # Add a legend
# legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
# ax.legend(prop=legend_font)

# plt.tight_layout()

# # plt.savefig(file[:-4]+'.pdf', format='pdf', bbox_inches='tight')
# # plt.savefig(file[:-4]+'.png', format='png', bbox_inches='tight')
# # Show the plot
# plt.show()


import matplotlib.pyplot as plt
import numpy as np

file = r"D:\Inversion Data\Nb3Sn\Nb3Sn8105\Nb3Sn8105_J.mat"

# Importing The Matrix
matrix = np.loadtxt(file, comments='#')

# Print the shape
num_rows, num_columns = matrix.shape
print(f"Number of rows: {num_rows}\nNumber of columns: {num_columns}")

# Flatten the matrix to a 1D array
data_flat = matrix.flatten()

# Create a figure and axes
fig, ax = plt.subplots(figsize=(10, 8))

exponent = 10
normal_value = 1 * 10 ** exponent

# Calculate the histogram values
# Plot the histogram as a line
hist_values, bins, _ = plt.hist(data_flat/normal_value, bins=50, color='orange', edgecolor='black', density=True, alpha=1)
ax.plot(bins[:-1], hist_values, color='red', linestyle='-', linewidth=5, label="J$_c^L$")


# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}

# Set x-axis label with proper formatting
ax.set_xlabel('J$_c^L$ ($\\times 10^{{{}}}$ A/m$^2$)'.format(exponent), fontdict)

# Set y-axis label
ax.set_ylabel('Probability Density', fontdict)

# Add a legend
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.legend(prop=legend_font)

plt.tight_layout()

# plt.savefig(file[:-4]+'.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(file[:-4]+'.png', format='png', bbox_inches='tight')
# Show the plot
plt.show()


