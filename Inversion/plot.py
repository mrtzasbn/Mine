# -*- coding: utf-8 -*-

import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


#==============================================================================

def find_exp(number):
    base10 = math.log10(abs(number))
    return abs(math.floor(base10))

def iMatrix(filetoread):

    # open file
    f = open(filetoread, 'r')

    s = [ [ float(i) for i in line.split() ] for line in f if line[0] != '#' ]
    
    return np.array(s)

#============================Scanparameters====================================
#Thickness: 3 µm
#Distance: 10 µm
#Stepsize: 50 µm
# D:/Data/Inversion Data/R192-5/coarse_30_30_50_5K.dat
#==============================================================================

samples=[]

sample={
    'fil':"coarse_30_30_50_5K",
    'path':"D:/Data/Inversion Data/R192-5/",          
       }    
samples.append(sample)


for sample in samples:

    fil = sample['fil']
    path = sample['path']

    filetoread = path+fil+'/'+fil+'_J.mat'
    filetoreadx = path+fil+'/'+fil+'_Jx.mat'
    filetoready = path+fil+'/'+fil+'_Jy.mat'
    
    J = iMatrix(filetoread)
    Jx = iMatrix(filetoreadx)
    Jy = iMatrix(filetoready)
    
    A, B = np.meshgrid(np.arange(0, np.shape(Jx)[1]), np.arange(0, np.shape(Jx)[0]))
    
    #==============================================================================
    
    fig = plt.figure(figsize=(7, 6))
    plt.rc('font', **{'size':'14'})
    ax = fig.add_subplot(111)
    
    # image
    power = int(find_exp(np.mean(J)))
    power_str = str(power)
    im = ax.imshow(J*10**-power,
                    origin = 'upper',
                    cmap = 'viridis',
                    interpolation="bicubic")
    shape = np.shape(J)
    print(shape)
    # colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.2)
    cbar= plt.colorbar(im, cax=cax)
    cbar.ax.tick_params(labelsize=12)
    # cbar.ax.set_ylabel('$\it{J}$$\mathrm{_c}\mathrm{^L}$ x $10^{'+power_str+'}$ (A/m$^{2}$)')
    cbar.ax.set_ylabel('$\\it{J}$$\mathrm{_c}\mathrm{^L}$ x $10^{'+power_str+'}$ (A/m$^{2}$)')
    cbar001 = np.percentile(J*10**-power, 0.01)    
    cbar999 = np.percentile(J*10**-power, 99.9)    
    im.set_clim(cbar001, cbar999)
    
    #remove ticks
    ax.axis('off')
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)

    
    # plot arrows
    n=1
    ax.quiver(A[::n, ::n],B[::n, ::n],Jx[::n, ::n],Jy[::n, ::n],headwidth = 5, minlength = 3, color = "indigo", angles ='xy', scale=2e1*np.max(J))

    
    # ax.hlines(y=97, xmin=70, xmax=90, color='w', linewidth=2.5)
    # ax.text(80,94,'1 mm', horizontalalignment='center', verticalalignment='center', color='w', size=18)
    ax.set_aspect(shape[1]/shape[0])
    plt.tight_layout()
    # fig.savefig(path+fil+'_J.pdf', dpi=300, bbox_inches = "tight")
    # fig.savefig(path+fil+'_J.png', dpi=300, bbox_inches = "tight")
    plt.show()


