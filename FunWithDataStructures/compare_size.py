import numpy as np
import pandas as pd
import xarray as xr
from matplotlib import pyplot as plt

def create_data(nof_values):
    """ Create a dataset with random values.

    Parameters
    ----------
    nof_values : int
        dataset will contain nof_values * 2 values.

    Returns
    -------
    data : xarray.Dataset
    """
                        
    data = xr.Dataset({'x':np.random.randn(nof_values), 
                       'y':np.random.randn(nof_values)})

    return data


def save_all_formats(data):
    """ Saves data in all formats (csv, json, hdf5, netcdf).

    Parameters
    ----------
    data : xarray.Dataset

    Notes
    -----
    To store the data in csv and hdf5 we use pandas.
    """
    df = data.to_dataframe()

    # csv   
    df.to_csv("RandomData.csv")

    # json
    json_out = df.reset_index().to_json(orient='records')
    with open('RandomData.json', 'w') as f:
        f.write(json_out)
        f.close()

    # hdf5
    df.to_hdf("RandomData.h5", 'data')

    # netcdf
    data.to_netcdf("RandomData.nc")

def main():
    data = create_data(1000)

#    plt.scatter(data['x'], data['y'])
#    plt.show()

    save_all_formats(data)

if __name__ == '__main__':
    main()
