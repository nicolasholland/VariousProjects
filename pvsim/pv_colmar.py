#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import pvlib
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.modelchain import ModelChain

import matplotlib.pyplot as plt

import imageio
from io import BytesIO

location = Location(38.459, 7.22, 'Europe/Paris', 700, 'Colmar')
times = pd.date_range("2019-08-26", "2019-08-27", freq="1min")

cs = location.get_clearsky(times)

temp = np.array([22, 19, 18, 19, 26, 30, 31, 27, 23])
t = interp1d(np.arange(len(temp)), temp)
temp = t(np.linspace(0, len(temp)-1, len(cs)))

cs["temp_air"] = temp


# Shading
# No shadow at sec 17 - 24.
# Shadow starts again at sec. 41 - 48
ms, me = 17 * 25, 24*25
shadowm = np.linspace(.8, .1, num=me-ms)
cs.iloc[ms:me]['ghi'] = (cs['ghi'] - cs['dni']).iloc[ms:me] + shadowm * cs['dni'].iloc[ms:me]
cs.iloc[ms:me]['dni'] = shadowm * cs['dni'].iloc[ms:me]

es, ee = 41 * 25, 48*25
shadowe = np.linspace(.1, .8, num=ee-es)
cs.iloc[es:ee]['ghi'] = (cs['ghi'] - cs['dni']).iloc[es:ee] + shadowe * cs['dni'].iloc[es:ee]
cs.iloc[es:ee]['dni'] = shadowe * cs['dni'].iloc[es:ee]

sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
sandia_module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
cec_inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208_208V__CEC_2014_']


system = PVSystem(surface_tilt=20, surface_azimuth=188,
                  module_parameters=sandia_module,
                  inverter_parameters=cec_inverter)
mc = ModelChain(system, location)

mc.run_model(times=cs.index, weather=cs)
ac = mc.ac
ac[ac.isna()] = 0

def plotstuff(stop):
    fig, ax1 = plt.subplots(figsize=(15,10))
    ax2 = ax1.twinx()
    
    ts1 = ac.copy()
    ts2 = cs.temp_air.copy()

    ts1.index += pd.Timedelta("2h")
    ts2.index += pd.Timedelta("2h")
    
    ts1[stop:] = np.nan
    ts2[stop:] = np.nan
    
    ts1.plot(ax=ax1, linewidth=4, alpha=.8, color="blue")
    ts2.plot(ax=ax2, color="red", linewidth=4, alpha=.8)

    ax1.set_ylabel("Power")
    ax2.set_ylabel("Temperature")

    ax2.set_ylim(0, 40)
    ax1.set_ylim(-5, 180)
    ax1.set_xlim(cs.index[0], cs.index[-1])

    buf = BytesIO()
    plt.savefig(buf, format="png", bboxes_inches='tight')
    #plt.savefig("%d.png"%(stop), format="png", bboxes_inches='tight')
    plt.close()

    buf.seek(0)
    return imageio.imread(buf)

def process_video():
    """ docstring """
    output = imageio.get_writer('result.mp4', fps=25)

    for frameid in range(0, len(ac)):
    #for frameid in range(0, 300):
        print(frameid)
        img = plotstuff(frameid)

        output.append_data(img)

    output.close()


if __name__ == '__main__':
    process_video()
