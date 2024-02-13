import matplotlib.pyplot as plt

# Example data
x_data = [1, 2, 3, 4, 5]
y_data = [10, 12, 15, 18, 20]
y_error = [1, 1.5, 2, 1.2, 1.8]  # Example error values for each y-data point

# Create a basic line plot
plt.plot(x_data, y_data, marker='o', linestyle='-')

# Add error bars using `errorbar` function
plt.errorbar(x_data, y_data, yerr=y_error, fmt='o', capsize=5, label='Data with Error Bars')

# Label your axes
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')

# Add a legend if you have multiple data series
plt.legend()

# Display the plot
plt.show()
