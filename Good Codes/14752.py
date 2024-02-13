import numpy as np
from ioHall import iHall
from gridData import gridData
from sg_filter import sg_filter_2d                                                                                                        
import matplotlib.pyplot as plt
from matplotlib import rc

width = 5.8*3
rc('figure', **{'figsize': [0.49*width, 0.4*width]})

font = {'size': 18}
rc('font', **font)

# load data
# =========                                                                                            
                             
k, d = [1, 0]


filetoread = r"D:\Ramin\Nb3Sn\SHMP\R81_5\fine_scan_5K_up_whole_rem.dat"


# V = Hall Voltage
# S = Strain Gauge

hall_constant = 46.15526288533297

x, y, z, V, S, T, t = iHall(filetoread)


X, Y, Z = gridData(x, y, -V)
X = X*1e-3#*1.38
Y = Y*1e-3#*1.38
# Z = ((Z))
Z = ((Z-9.85885e-05)*hall_constant)
   

x_min = np.amin(X)
x_max = np.amax(X)
y_min = np.amin(Y)  
y_max = np.amax(Y)

#Z001=np.percentile(Z, 0.01)
#Z999=np.percentile(Z, 99.9)
# filter image
# ============
#print 'start filtering'
Z = sg_filter_2d(Z, 5, 3)  # (z, window_size, order, derivative=None

#print 'done'

# plot image
# ==========
#c_min = np.floor(np.amin(Z))
#c_max = np.ceil(np.amax(Z))

#V = list(np.linspace(c_min, c_max, 15))

fig = plt.figure(0, tight_layout=True)
ax = plt.subplot(111)
ax.autoscale(True)

aspect = ((x_max-x_min)/(y_max-y_min))
Z050=np.percentile(Z, 0.01)
Z999=np.percentile(Z, 99.99)
#cont = 

cax = ax.imshow(1000*Z,
                origin='lower',
                interpolation='None',
                aspect=1.,
                cmap='viridis',
                )

#contour = ax.contour(Z,
#                     colors='black',
                     #extent=extent)
#cax.set_clim(vmin=c_min, vmax=c_max)
#cax.set_clim(Z050,Z999)
#cax.set_clim(4.8,5)
cax.set_extent([x_min, x_max, y_min, y_max])

cbar = fig.colorbar(cax)
cbar.ax.set_ylabel(r'B (mT)')

yticks = np.arange(0.5, 2.5, step=0.1)
xticks = np.arange(1.3, 2.5, step=0.1)
#plt.yticks(yticks)
#plt.xticks(xticks)
ax.set_xlim([x_max, x_min])
ax.set_ylim([y_min, y_max])


#C = ax.contour(X, Y, Z, V, extent=[x_min, x_max, y_min, y_max])
#colors='gray'
# limits


# label plot
ax.set_xlabel(r'X (mm)')
ax.set_ylabel(r'Y (mm)')

# plt.xlim(2.14, 0.85)
# plt.ylim(1.64, 1.85)

# plt.title(f"Nb$_3$Sn, whole sample,\nremnant, applied B = 1.5 T")
plt.title(f"Nb$_3$Sn, whole sample,\nremnant, applied B = 1.5 T,\nHall constant= {hall_constant:.2f} T/V")
ax.grid(linewidth=0.5)
plt.tight_layout()
# plt.savefig(filetoread[:-4]+'.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(filetoread[:-4]+'.png', format='png', bbox_inches='tight')
plt.show()
