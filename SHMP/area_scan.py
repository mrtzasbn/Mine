#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from ioHall import iHall
from gridData import gridData
from sg_filter import sg_filter_2d
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

width = 5.8 * 3
rc("figure", **{"figsize": [0.49 * width, 0.4 * width]})

font = {"size": 18}
rc("font", **font)

# load data
# =========

# k, d = [1, 0]

filetoread = (
    "D:/MyData/CERN/R192-5/SHMP/upper_edge_fine_5K_infield_ramp_50mT.dat"
)
title = "The remnant field profile at 5 K\nwith a spatial resolution of 10 μm"

# V = Hall Voltage
# S = Strain Gauge
x, y, z, V, S, T, t = iHall(filetoread)


X, Y, Z = gridData(x, y, V)


X = X * 1e-3  # *1.38
Y = Y * 1e-3  # *1.38
# Z = ((Z))
Z = (Z-0.0000804) * (42.18)


x_min = np.amin(X)
x_max = np.amax(X)
y_min = np.amin(Y)
y_max = np.amax(Y)


# Z001=np.percentile(Z, 0.01)
# Z999=np.percentile(Z, 99.9)
# filter image
# ============
# print 'start filtering'
Z = sg_filter_2d(Z, 5, 3)  # (z, window_size, order, derivative=None)

# print 'done'

# plot image
# ==========
# c_min = np.floor(np.amin(Z))
# c_max = np.ceil(np.amax(Z))

# V = list(np.linspace(c_min, c_max, 15))
fontdict = {"fontsize": 18, "fontweight": "regular", "fontfamily": "serif"}

fig = plt.figure(0, tight_layout=True)
ax = plt.subplot(111)
ax.autoscale(True)

aspect = (x_max - x_min) / (y_max - y_min)

Z050 = np.percentile(Z, 0.01)
Z999 = np.percentile(Z, 99.99)

# cont =

cax = ax.imshow(
    1000 * Z,
    origin="lower",
    interpolation="None",
    aspect=1.00,
    cmap="viridis",
    vmin=-5,
    vmax=150
)
# plt.axhline(y=2.09)
plt.axhline(y=2.09, color='red', linestyle='--')
# contour = ax.contour(Z,
#                     colors='black',
# extent=extent)
# cax.set_clim(vmin=c_min, vmax=c_max)
# cax.set_clim(Z050,Z999)
# cax.set_clim(4.8,5)
cax.set_extent([x_min, x_max, y_min, y_max])

cbar = fig.colorbar(cax)
font_properties = FontProperties(
    family="serif", style="normal", size=16
)  # Adjust font properties as needed

for tick in cbar.ax.get_yticklabels():
    tick.set_fontproperties(font_properties)
cbar.ax.set_ylabel(r"Field (mT)", fontdict)

# yticks = np.arange(0.5, 2.5, step=0.1)
# xticks = np.arange(1.3, 2.5, step=0.1)
# plt.yticks(yticks)
# plt.xticks(xticks)
ax.set_xlim([x_max, x_min])
ax.set_ylim([y_min, y_max])


# C = ax.contour(X, Y, Z, V, extent=[x_min, x_max, y_min, y_max])
# colors='gray'
# limits


# label plot

ax.set_xlabel(r'X (mm)', fontdict)
ax.set_ylabel(r'Y (mm)', fontdict)
# ax.axis('off')
tick_font = {"family": "serif", "size": 16, "weight": "regular"}
for tick in ax.get_xticklabels():
    tick.set(**tick_font)
for tick in ax.get_yticklabels():
    tick.set(**tick_font)
# plt.title(f"Nb$_3$Sn, whole sample,\nremnant, applied B = 1.5 T,\nHall constant= {36.96:.2f} T/V")
# ax.grid(linewidth=0.5)
# plt.tight_layout()

# ax.set_title(title, fontdict)

file_name_to_save = filetoread.split("/")[-1][:-4]
# file_name_to_save = file_name_to_save[-1][:-4]

ax.set_title(file_name_to_save, fontdict)
# plt.savefig(file_name_to_save+'scaled.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(file_name_to_save+'scaled.png', format='png', bbox_inches='tight')


plt.show()
