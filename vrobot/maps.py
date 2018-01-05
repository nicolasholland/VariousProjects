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


if __name__ == '__main__':
    b = box()
    b.plot()

    plt.show()
