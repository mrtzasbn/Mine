import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.ticker as ticker


x1 = np.arange(0, 1, 0.01)
x2 = np.arange(1, -1, -0.01)
x3 = np.arange(-1, 1.01, 0.01)

print(len(np.concatenate([x1, x2, x3])))
