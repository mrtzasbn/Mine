import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create a figure and axis
fig, ax = plt.subplots()

# Define the rectangle's bottom left corner, width, and height
bottom_left_corner = (2, 2)
width = 2
height = 1

# Create a Rectangle patch
rectangle = patches.Rectangle(bottom_left_corner, width, height, linewidth=1, edgecolor='r', facecolor='none')

# Add the rectangle to the Axes
ax.add_patch(rectangle)

# Set aspect ratio to be equal to prevent distortion
ax.set_aspect('equal', adjustable='box')

# Set labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Rectangle Example')

# Show the plot with the rectangle
plt.show()
