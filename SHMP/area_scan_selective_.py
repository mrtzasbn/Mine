#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from ioHall import iHall
from gridData import gridData
from sg_filter import sg_filter_2d
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.font_manager import FontProperties

# Your existing setup for figure size and font
width = 5.8 * 3
rc("figure", **{"figsize": [0.49 * width, 0.4 * width]})
font = {"size": 18}
rc("font", **font)

# Load data
filetoread = "D:/Data/SHMP/Nb3Sn ThinFilm/R81_5/Until 10 Nov 2023/fine_scan_5K_up_whole_rem.dat"
title = "The remnant field profile at 5 K\nwith a spatial resolution of 10 μm"
x, y, z, V, S, T, t = iHall(filetoread)
X, Y, Z = gridData(x, y, -V)
X = X * 1e-3
Y = Y * 1e-3
Z = Z

# Setting min and max for both axes
x_min, x_max = np.amin(X), np.amax(X)
y_min, y_max = np.amin(Y), np.amax(Y)

# Filter image using Savitzky-Golay filter
Z = sg_filter_2d(Z, 5, 3)

# Prepare to plot
fig = plt.figure(0, tight_layout=True)
ax = plt.subplot(111)
ax.autoscale(True)
aspect = (x_max - x_min) / (y_max - y_min)
fontdict = {"fontsize": 18, "fontweight": "regular", "fontfamily": "serif"}

# Define the center and radius of the circle
center_x = (x_max + x_min) / 2
center_y = (y_max + y_min) / 2
radius =0.5  # Choose the smaller range to ensure circle is within both

# Generate theta values from 0 to 2*pi to create a circle
theta = np.linspace(0, 2*np.pi, 100)

# Calculate the x and y coordinates of the circle
x = center_x + radius * np.cos(theta)
y = center_y + radius * np.sin(theta)

# Plot the circle
ax.plot(x, y, label='Circle', color='white', zorder=1, linewidth=3)

# Set aspect ratio to be equal, ensuring the circle is not distorted
ax.set_aspect('equal', adjustable='box')

# Mask for points inside the circle
mask = (X - center_x) ** 2 + (Y - center_y) ** 2 < radius ** 2
Z_masked = np.ma.masked_where(~mask, Z)

# Plot only the masked (inside circle) data
cax = ax.imshow(
    1000 * Z,
    origin="lower",
    interpolation="None",
    aspect='equal',
    cmap="viridis",
)
cax.set_extent([x_min, x_max, y_min, y_max])

# Colorbar formatting
cbar = fig.colorbar(cax)
font_properties = FontProperties(family="serif", style="normal", size=16)
for tick in cbar.ax.get_yticklabels():
    tick.set_fontproperties(font_properties)
cbar.ax.set_ylabel(r"Field (mT)", fontdict)

# Set the labels
ax.set_xlabel(r'X (mm)', fontdict)
ax.set_ylabel(r'Y (mm)', fontdict)
ax.set_title(title, fontdict)
ax.axis('off')
# Set the ticks (optional if you want different ticks than the default)
tick_font = {"family": "serif", "size": 16, "weight": "regular"}
for tick in ax.get_xticklabels() + ax.get_yticklabels():
    tick.set(**tick_font)

# # Plot the circle for visual reference (if desired)
# theta = np.linspace(0, 2 * np.pi, 100)
# circle_x = center_x + radius * np.cos(theta)
# circle_y = center_y + radius * np.sin(theta)
# ax.plot(circle_x, circle_y, color='red')

plt.show()
