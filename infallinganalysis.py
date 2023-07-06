#importing everything
from analysis import * 
from compiler import *
import pynbody
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filenames = {'h148': '/home/watanabe/Sims/h148.cosmo50PLK.3072g/h148.cosmo50PLK.3072g3HbwK1BH/snapshots_200crit_h148/h148.cosmo50PLK.3072g3HbwK1BH.004096',
            'h229': '/home/watanabe/Sims/h229.cosmo50PLK.3072g/h229.cosmo50PLK.3072gst5HbwK1BH/snapshots_200crit_h229/h229.cosmo50PLK.3072gst5HbwK1BH.004096',
            'h242': '/home/watanabe/Sims/h242.cosmo50PLK.3072g/h242.cosmo50PLK.3072gst5HbwK1BH/snapshots_200crit_h242/h242.cosmo50PLK.3072gst5HbwK1BH.004096',
            'h329': '/home/watanabe/Sims/h329.cosmo50PLK.3072g/h329.cosmo50PLK.3072gst5HbwK1BH/snapshots_200crit_h329/h329.cosmo50PLK.3072gst5HbwK1BH.004096'}


def calc_sfr(key):
    """
    This reads the original snapshots of sim data and returns the sfr over the same time range as tracked_particle data
    """
    
    #read the original data source
    sim, haloid = str(key[:4]), int(key[5:])
    data = read_tracked_particles(sim, haloid)
    tmin, tmax = np.min(data.time), np.max(data.time)
    n = len(np.unique(data.time))

    #load the data
    s = pynbody.load(filenames[sim])
    h = s.halos()

    halo = h.load_copy(haloid)
    simstars = halo.s

    #find the star formation rate
    #following code is inherited from pynbody.plot.stars.sfh
    #the difference is that the range of time is based on data.time, not sim time
    bins = n
    trange = [tmin, tmax]
    binnorm = 1e-9 * bins / (trange[1] - trange[0])

    #filter out simstars out of data.time range
    trangefilt = pynbody.filt.And(pynbody.filt.HighPass('tform', str(trange[0]) + ' Gyr'),
                          pynbody.filt.LowPass('tform', str(trange[1]) + ' Gyr'))
    tforms = simstars[trangefilt]['tform'].in_units('Gyr')
    
    weight = simstars[trangefilt]['mass'].in_units('Msol') * binnorm
    sfr, thebins = np.histogram(tforms, weights=weight, bins=bins)
    
    print(f'> Returning (sfr) variable for {key} <')
    
    return sfr, thebins