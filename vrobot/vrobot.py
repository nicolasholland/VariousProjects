import numpy as np
import matplotlib.pyplot as plt

import maps

class vrobot:
    """
    A virtual robot.
    """
    def __init__(self, x, y):
        """
        Init robot with position.

        Parameters
        ----------
        x : float
        y : float
        """
        self.position = np.array([x, y])

    def scan(self, nofrays=20, length=5):
        """
        Scan surroundings.

        Parameters
        ----------
        nofrays : int, default 20
        length : float, default 2
        """
        rays = np.array([[np.cos(x), np.sin(x)] for x in np.linspace(0, 2*np.pi,
                                                                     nofrays)])
        self.rays = rays * length

    def reflect(self, maps):
        """
        compares rays from scan with current map to get intersections.

        Parameters
        ----------
        maps : maps object
        """
        points = np.array([])
        for i in range(len(self.rays)):
            ray = np.array([self.position, self.rays[i]])
            for j in range(len(maps.sides)):
                wall = maps.sides[j]

                inter = r.intersect(ray, wall)

                if inter is not None:
                    points = np.append(points, inter)
                    break

        self.points = points.reshape(int(len(points)/2), 2)

    def plot(self):
        """
        plot rays
        """
        for point in self.points:
            plt.plot([self.position[0], point[0]], [self.position[1], point[1]],
                     color='black')

        for point in self.points:
            plt.plot(point[0], point[1], 'o', color='red')

        plt.plot(self.position[0], self.position[1], 'o', color='green')

    def features(self):
        """
        Lengths of reflected rays.
        """
        return np.array([np.sqrt((self.position[0] - point[0])**2 +
                                 (self.position[1] - point[1])**2)
                         for point in self.points])

    def intersect(self, ray, wall, tol=.01):
        """
        compute intersection of ray and wall.

        Parameters
        ----------
        ray : np.array
        wall : np.array
        """
        assert(ray.shape == (2, 2))
        assert(wall.shape == (2, 2))

        L1 = self.__line(ray[0], ray[1])
        L2 = self.__line(wall[0], wall[1])

        R = self.__intersection(L1, L2)
        if R:
            sray1 = np.copy(ray[:, 0])
            sray1.sort()

            sray2 = np.copy(ray[:, 1])
            sray2.sort()

            swall1 = np.copy(wall[:, 0])
            swall1.sort()

            swall2 = np.copy(wall[:, 1])
            swall2.sort()

            if (R[0] > sray1[0] and R[0] < sray1[1] and
                R[1] > sray2[0] and R[1] < sray2[1] and
                R[0] > swall1[0]-tol and R[0] < swall1[1]+tol and
                R[1] > swall2[0]-tol and R[1] < swall2[1]+tol):
                return np.array(R)

    @staticmethod
    def __line(p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C

    @staticmethod
    def __intersection(L1, L2):
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return x,y
        else:
            return False

if __name__ == '__main__':
    b = maps.simple_sketch()
    r = vrobot(.5, -.5)

    r.scan()
    r.reflect(b)

    b.plot()
    r.plot()

    print(r.features())

    plt.axis([-6, 2, -2, 4])
    plt.show()
