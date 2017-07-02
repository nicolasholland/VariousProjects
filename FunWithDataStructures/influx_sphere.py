import argparse
from influxdb import InfluxDBClient
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, timedelta


def create_sphere_data(r=10, step=1, half=False):
    """ Creates data structured in a sphere.

    Parameters
    ----------
    r : int
        default 10
    step : int
        default 1
    half : bool
        default False

    Returns
    -------
    data : <class numpy.ndarray>
    """
    zero = datetime(2017, 7, 1, 0, 0)
    delta = timedelta(minutes=10)
    data = np.array([0, 0, -r, np.random.random(), zero])

    # loop over all possible points
    for x in range(-r, r, step):
        for y in range(-r, r, step):
            for z in range(-r+1, r+1  , step):
                if np.sqrt(x**2 + y**2 + z**2) > r:
                    continue

                if half and z == 0:
                    break

                data = np.vstack((data, np.array([x, y, z, np.random.random(),
                                  zero+z*delta +
                                  timedelta(seconds=np.random.randint(1, 60)) ])))

    return data

def plot_sphere_data(data):
    """ Uses matplotlib to plot sphere data.

    Parameters
    ----------
    data : <class numpy.ndarray>
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(data[:, 0].astype(np.int32), data[:, 1].astype(np.int32),
               data[:, 2].astype(np.int32), c=data[:, 3].astype(np.float32))

    plt.show()


def point_to_json(point):
    """ Creates json strings.

    Parameters
    ----------
    point : <class numpy.ndarray>

    Returns
    -------
    json : dict
    """
    json = [
        {
            "measurement": "event_in_the_universe",
            "time": "%s" %point[4],
            "fields": {
                "x": point[0],
                "y": point[1],
                "z": point[2],
                "event": point[3],
            }
        }
    ]
    return json


def json_to_point(json):
    """ Inverse to point_to_json.

    Parameters
    ----------
    json : dict

    Returns
    -------
    point : <class numpy-ndarray>
    """

    point = np.array([int(json['x']), int(json['y']), int(json['z']),
                     float(json['event']), json['time']])
    return point


def main():
    # open database
    client = InfluxDBClient(host='127.0.0.1', port=8086, database='sphere')

    # create data and store it
    #data = create_sphere_data(r=5, step=1, half=False)
    #plot_sphere_data(data)

    #for point in data:
    #    json = point_to_json(point)
    #    client.write_points(json)

    # retrieve data and plot it
    query = 'select * from event_in_the_universe;'
    rs = client.query(query)
    rs = list(rs.get_points())

    data = json_to_point(rs[0])
    for point in rs[1:]:
        data = np.vstack((data, json_to_point(point)))

    plot_sphere_data(data)

    # delete table
#    client.drop_database('sphere')


if __name__ == '__main__':
    main()
