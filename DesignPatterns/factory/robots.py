import abc

class Robot(metaclass=abc.ABCMeta):
    """
    Define abstract robot class.
    """
    @abc.abstractmethod
    def whoami(self):
        pass

class Humanoid(Robot):
    """
    A humanoid robot has arms, legs and looks like a human.
    """
    @staticmethod
    def whoami():
        return "I have arms, legs and look like a human."

class Drone(Robot):
    """
    A drone can fly and has a camera to take pictures.
    """
    @staticmethod
    def whoami():
        return "I can fly and have a camera to take pictures."
    
class Bot(Robot):
    """
    A bot lives in the internet and produces tweets.
    """
    @staticmethod
    def whoami():
        return "I live in the internet and produce tweets."
