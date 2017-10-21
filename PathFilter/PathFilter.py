import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numba import jit


@jit
def filter_artefact(point, pre, suc, param=.71):
    """
    Given a point, its pre- and successor this function decides if it is an
    artefact.

    Parameters
    ----------
    point : np.array([x, y])
    pre : np.array([x, y])
    suc : np.array([x, y])
    param : float, default is 0.71

    Returns
    -------
    bool, False if point is an artefact, True if not.
    """
    presuc_length = np.sqrt((suc[0] - pre[0])**2 + (suc[1] - pre[1])**2)

    if presuc_length < 0.00001:
        c_length = np.sqrt((point[0] - pre[0])**2 + (point[1] - pre[1])**2)

    # Make sure divisor values are not too small
    elif ((suc[0] - pre[0])/presuc_length > 0.001) and ((suc[1] - pre[1])/presuc_length > 0.001):
        pre2suc_rise = (suc[1] - pre[1])/(suc[0] - pre[0])
        rise = -1 / pre2suc_rise

        # Compute Point where lines meet
        const_c = point[1] - rise * point[0]
        const_ps = pre[1] - pre2suc_rise * pre[0]

        x_schnitt = (const_c - const_ps)/(pre2suc_rise - rise)
        y_schnitt = x_schnitt * pre2suc_rise + const_ps

        c_length = np.sqrt((x_schnitt - point[0])**2 +
                           (y_schnitt - point[1])**2)

    elif ((suc[0] - pre[0])/presuc_length  > 0.001):
        c_length = np.abs(point[0] - suc[0])

    else:
        c_length = np.abs(point[1] - suc[1])

    if c_length > param * presuc_length:
        return False

    return True


@jit
def main(path):
    """
    Removes artefacts from path

    Parameters
    ----------
    path : numpy array with shape [N, 2]

    Returns
    -------
    path : numpy array
    """
    mask = np.ones(path.shape[0], dtype=bool)
    for it in range(1, path.shape[0]-1):
        mask[it] = filter_artefact(path[it], path[it-1], path[it+1])
    return path[mask]


if __name__ == '__main__':
    df = pd.read_csv(sys.argv[1], delimiter=';', header=None)
    path = np.column_stack((np.asarray(df[0]), np.asarray(df[1])))

    path = main(path)
    plt.plot(path[:, 0], path[:, 1])

    frame1 = plt.gca()
    frame1.axes.xaxis.set_ticklabels([])
    frame1.axes.yaxis.set_ticklabels([])
    plt.show()
