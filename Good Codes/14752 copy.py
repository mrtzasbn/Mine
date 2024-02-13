import numpy as np
from ioHall import iHall
from gridData import gridData
from sg_filter import sg_filter_2d                                                                                                        
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd

width = 5.8*3
rc('figure', **{'figsize': [0.49*width, 0.4*width]})

font = {'size': 18}
rc('font', **font)

# load data
# =========                                                                                            
                             
k, d = [1, 0]


# Specify the file path
file_path = r"D:\Ramin\Nb3Sn\SHMP\R81_5\fine_scan_5K_up_edge_rem.dat"

# Read the data into a DataFrame
df = pd.read_csv(file_path, delim_whitespace=True, skiprows=19, names=['x(µm)', 'y(µm)', 'z(µm)', 'V_hall(V)', 'V_cant(V)', 'T(K)', 'time(s)'], encoding='latin1')

# Display the DataFrame
print(df)