import numpy as np
from scipy.interpolate import griddata


def gridData(x, y, z, **kwds):
    # check for keyword
    method = kwds.get('method') if 'method' in kwds else 'linear'
    f = kwds.get('f') if 'f' in kwds else 1.
    # get the shape of the image
    npx, npy = [len(x), len(max(x, key=len))]
    # convert to 1-D array
    x = np.array([j for i in x for j in i])
    y = np.array([j for i in y for j in i])
    z = np.array([j for i in z for j in i])
    # set regular grid
    xi = np.linspace(x.min(), x.max(), int(npx*f))
    yi = np.linspace(y.min(), y.max(), int(npy*f))
    # generate X and Y grid
    X, Y = np.meshgrid(xi, yi)
    # Array of (x,y) position vectors
    points = np.array([x, y]).T
    # Array of (z) values
    values = z
    # generate uniform spaced grid
    grid = griddata(points, values, (X, Y), method=method)
    # remove all 'NaN'
    while np.isnan(grid).sum() != 0:
        ax_0 = np.isnan(grid).sum(axis=0)
        ax_1 = np.isnan(grid).sum(axis=1)
        if ax_0.max() > ax_1.max():
            grid = np.delete(grid, np.argmax(ax_0), axis=1)
            X = np.delete(X, np.argmax(ax_0), axis=1)
            Y = np.delete(Y, np.argmax(ax_0), axis=1)
        else:
            grid = np.delete(grid, np.argmax(ax_1), axis=0)
            X = np.delete(X, np.argmax(ax_1), axis=0)
            Y = np.delete(Y, np.argmax(ax_1), axis=0)
    return X, Y, grid
