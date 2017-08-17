import sys
import numpy as np
import matplotlib.pyplot as plt

class Dot:
    def __init__(self):
        self.current_x = 0
        self.current_y = 0

        self.speed_x = np.random.random()
        self.speed_y = np.random.random()        

        self.path_x = np.array([0])
        self.path_y = np.array([0])

    def store(self):
        self.path_x = np.append(self.path_x, self.current_x)
        self.path_y = np.append(self.path_y, self.current_y)

    def update(self, smooth):
        self.current_x += self.speed_x
        self.current_y += self.speed_y

        self.speed_x = smooth * self.speed_x + np.random.random() - 0.5
        self.speed_y = smooth * self.speed_y + np.random.random() - 0.5

    def move(self, n=10, smooth=0):
        for step in range(n):
            self.update(smooth)
            self.store()

    def plot_path(self):
        plt.plot(self.path_x, self.path_y)

def main(smooth, nofdots):
    for it in range(nofdots):
        d = Dot()

        d.move(1000, smooth)

        d.plot_path()

    plt.show()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        msg = 'Use with %s <smoothing> <nofdots>' %(sys.argv[0])
        sys.exit(msg)
    main(float(sys.argv[1]), int(sys.argv[2]))
