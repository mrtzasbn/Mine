import matplotlib.pyplot as plt
import numpy as np

# Create a figure and axis
fig, ax = plt.subplots()

# Draw a rectangle
# Define the coordinates of the rectangle's bottom-left corner
x_bottom_left = 1
y_bottom_left = 1

# Define the width and height of the rectangle
width = 2
height = 3

# Create an array of x and y coordinates for the rectangle
x_rect = [x_bottom_left, x_bottom_left + width, x_bottom_left + width, x_bottom_left, x_bottom_left]
y_rect = [y_bottom_left, y_bottom_left, y_bottom_left + height, y_bottom_left + height, y_bottom_left]

# Plot the rectangle
ax.plot(x_rect, y_rect, label='Rectangle')

# Set aspect ratio to be equal, ensuring the rectangle is not distorted
ax.set_aspect('equal', adjustable='box')

# Set labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Rectangle Example')

# Display the legend
ax.legend()

# Show the plot
plt.show()
