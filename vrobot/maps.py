import numpy as np
import matplotlib.pyplot as plt

class map:
    """ base class for our room maps"""
    def plot(self):
        """
        plot map
        """
        for side in self.sides:
            plt.plot(side[:, 0], side[:, 1], color='black')

class box(map):

    """ a box """
    def __init__(self, hlen=1):
        s1 = np.array([-1, -1, -1, 1]).reshape(2,2)

        s2 = np.array([1, -1, 1, 1]).reshape(2,2)

        s3 = np.array([-1, -1, 1, -1]).reshape(2,2)

        s4 = np.array([-1, 1, 1, 1]).reshape(2,2)

        self.sides = np.array([s1, s2, s3, s4])

class simple_sketch(map):
    """ simplified sketch """
    def __init__(self):
        s1 = np.array([-1, -1, -1, 1]).reshape(2,2)
        s2 = np.array([1, -1, 1, 1]).reshape(2,2)
        s3 = np.array([-1, -1, 1, -1]).reshape(2,2)
        s4 = np.array([0, 1, 1, 1]).reshape(2,2)
        s5 = np.array([-1, 1, -5, 1]).reshape(2,2)
        s6 = np.array([0, 1, 0, 2]).reshape(2,2)
        s7 = np.array([0, 2, -3.5, 2]).reshape(2,2)
        s8 = np.array([-5, 1, -5, 3]).reshape(2,2)
        s9 = np.array([-5, 3, -3.5, 3]).reshape(2,2)
        s10 = np.array([-3.5, 3, -3.5, 2]).reshape(2,2)

        self.sides = np.array([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10])


if __name__ == '__main__':
    b = simple_sketch()
    b.plot()

    plt.axis([-6, 2, -2, 4])
    plt.show()
