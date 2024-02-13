import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = r"D:\Ramin\Nb3Sn\R81_5\area_fine_5K_if.dat"
# Sample DataFrame (replace this with your actual DataFrame)
data = pd.read_csv(
                file_path, delim_whitespace=True, comment='#', header=None,
                names=["x(µm)", "y(µm)", "z(µm)", "V_hall(V)", "V_cant(V)", "T(K)", "time(s)"]
                 )

# Extract x, y, and V columns from the DataFrame
x = data['x']
y = data['y']
V = data['V']

# Determine the dimensions of the grid
x_min, x_max = x.min(), x.max()
y_min, y_max = y.min(), y.max()

# Create a grid of zeros to represent the color map
grid = np.zeros((y_max - y_min + 1, x_max - x_min + 1))

# Fill the grid with V values
for xi, yi, vi in zip(x, y, V):
    grid[y_max - yi, xi - x_min] = vi

# Create a plot using ax.imshow()
fig, ax = plt.subplots()
cax = ax.imshow(grid, cmap='viridis', extent=[x_min, x_max, y_min, y_max], aspect='auto', origin='upper')

# Add labels and colorbar
plt.xlabel('X-Axis')
plt.ylabel('Y-Axis')
plt.title('Heatmap of V Values')
plt.colorbar(cax, label='V')

# Show the plot
plt.show()
