import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import gridData


# Provide the file path
file_path = r"D:\Ramin\Nb3Sn\R81_5\area_coarse_5k_if.dat"

# Read the data from the file, skipping lines starting with '#'

area_scan = pd.read_csv(
                file_path, delim_whitespace=True, comment='#', header=None,
                names=["x(µm)", "y(µm)", "z(µm)", "V_hall(V)", "V_cant(V)", "T(K)", "time(s)"]
                 )


width = 5.8*3
rc('figure', **{'figsize': [0.49*width, 0.4*width]})

font = {'size': 18}
rc('font', **font)
                                                                                         
                             
k, d = [1, 0]



# V = Hall Voltage
# S = Strain Gauge
# x, y, z, V, S, T, t = area_scan



#x_tmp = []
#y_tmp = []
#V_tmp = []
#for i in range(5, len(V)):
#    x_tmp.append([])
#    y_tmp.append([])
#    V_tmp.append([])
#    for j in range(len(V[i])):
#        if V[i][j] < 1e10:
#            x_tmp[-1].append(x[i][j])x
#            y_tmp[-1].append(y[i][j])
#            V_tmp[-1].append(V[i][j])
#
#X, Y, Z = gridData(x_tmp, y_tmp, V_tmp)

X, Y, Z = gridData(area_scan["x(µm)"], area_scan["y(µm)"], -area_scan["V_hall(V)"])
X = X*1e-3#*1.38
Y = Y*1e-3#*1.38
Z = ((Z))
#Z = ((Z+5.41251e-04)*55*1e3)
   

x_min = np.amin(X)
x_max = np.amax(X)
y_min = np.amin(Y)  
y_max = np.amax(Y)

#Z001=np.percentile(Z, 0.01)
#Z999=np.percentile(Z, 99.9)
# filter image
# ============
#print 'start filtering'
# Z = sg_filter_2d(Z, 5, 3)  # (z, window_size, order, derivative=None

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

cax = ax.imshow(Z,
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
cbar.ax.set_ylabel(r'U (V)')

#yticks = np.arange(0.5, 2.5, step=0.1)
#xticks = np.arange(1.3, 2.5, step=0.1)
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

ax.grid(linewidth=0.5)
plt.tight_layout()
# plt.savefig(filetoread[:-4]+'.pdf', format='pdf', bbox_inches='tight')
# plt.savefig(filetoread[:-4]+'.png', format='png', bbox_inches='tight')
plt.show()

#fig.savefig('C:/DATA/Sigrid/EuRb1144/Crystal5/ab/area1_fieldcooled_20mT_5K_corr.pdf')
#fig.savefig('C:/DATA/Sigrid/EuRb1144/Crystal5/ab/area1_meissner_3mT_5K.pdf')