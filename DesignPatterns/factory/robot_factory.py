from robots import *

def robot_factory(robot):
    """
    Simple robot factory function.
    """
    print('Building robot of type %s:'%(robot))
    return eval(robot)

def main():
    humanoid_robot = robot_factory('Humanoid')
    print(humanoid_robot.whoami())

    drone_robot = robot_factory('Drone')
    print(drone_robot.whoami())

    drone_robot = robot_factory('Bot')
    print(drone_robot.whoami())

if __name__ == '__main__':
    main()
