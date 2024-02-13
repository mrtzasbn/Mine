import matplotlib.pyplot as plt
import numpy as np

file = r"F:\Ramin\rem_whole\rem_whole_J.mat"

# Importing The Matrix
matrix = np.loadtxt(file, comments='#')

# Print the shape
rows, cols = matrix.shape

for i in range(rows):
    for j in range(cols):
        if ((i-64)**2)+ ((j-64)**2) < 3390:
            subset_matrix = matrix[:i, :j]
            data_flat = subset_matrix.flatten()




# Create a figure and axes
fig, ax = plt.subplots(figsize=(10, 8))

exponent = 10
normal_value = 1 * 10 ** exponent
# Plot the histogram
ax.hist(data_flat/normal_value, bins=50, color='green', edgecolor='black', density=True, label="J$_x$")

# Customize labels, titles, fonts, and legend
fontdict = {'fontsize': 14, 'fontweight': 'regular', 'fontfamily': 'serif'}

# Set x-axis label with proper formatting
ax.set_xlabel('J$_x$ ($\\times 10^{{{}}}$ A/m$^2$)'.format(exponent), fontdict)

# Set y-axis label
ax.set_ylabel('Probability Density', fontdict)

# Add a legend
legend_font = {'family': 'serif', 'size': 12, 'weight': 'regular'}
ax.legend(prop=legend_font)

plt.tight_layout()

# Show the plot
plt.show()




