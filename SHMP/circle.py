import matplotlib.pyplot as plt
import numpy as np

# Create a figure and axis
fig, ax = plt.subplots()

# Define the center and radius of the circle
center = (0, 0)
radius = 1

# Generate theta values from 0 to 2*pi to create a circle
theta = np.linspace(0, 2*np.pi, 100)

# Calculate the x and y coordinates of the circle
x = center[0] + radius * np.cos(theta)
y = center[1] + radius * np.sin(theta)

# Plot the circle
ax.plot(x, y, label='Circle')

# Set aspect ratio to be equal, ensuring the circle is not distorted
ax.set_aspect('equal', adjustable='box')

# Set labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Circle Example')

# Display the legend
ax.legend()

# Show the plot
plt.show()
