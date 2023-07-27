#import everything
import pynbody
import numpy as np
import pandas as pd
import pickle
import tqdm
from analysis import * 
from compiler import *

G = 6.6743015*10**(-11) #grav constant in units of N kg-2 m2

#make sure to use AHF otherwise it prioritizes AmgiaGrpCatalogue and you lose a lot of important info
pynbody.config['halo-class-priority'] = [pynbody.halo.ahf.AHFCatalogue,pynbody.halo.GrpCatalogue,
  pynbody.halo.AmigaGrpCatalogue,
  pynbody.halo.legacy.RockstarIntermediateCatalogue,
  pynbody.halo.rockstar.RockstarCatalogue,
  pynbody.halo.subfind.SubfindCatalogue,
  pynbody.halo.adaptahop.NewAdaptaHOPCatalogue,
  pynbody.halo.adaptahop.AdaptaHOPCatalogue,
  pynbody.halo.hop.HOPCatalogue,
  pynbody.halo.subfindhdf.Gadget4SubfindHDFCatalogue,
  pynbody.halo.subfindhdf.ArepoSubfindHDFCatalogue]

#read original sim dataset
filenames = {'h148': '/home/watanabe/Sims/h148.cosmo50PLK.3072g/h148.cosmo50PLK.3072g3HbwK1BH/snapshots_200crit_h148/h148.cosmo50PLK.3072g3HbwK1BH.004096',
            'h229': '/home/watanabe/Sims/h229.cosmo50PLK.3072g/h229.cosmo50PLK.3072gst5HbwK1BH/snapshots_200crit_h229/h229.cosmo50PLK.3072gst5HbwK1BH.004096',
            'h242': '/home/watanabe/Sims/h242.cosmo50PLK.3072g/h242.cosmo50PLK.3072gst5HbwK1BH/snapshots_200crit_h242/h242.cosmo50PLK.3072gst5HbwK1BH.004096',
            'h329': '/home/watanabe/Sims/h329.cosmo50PLK.3072g/h329.cosmo50PLK.3072gst5HbwK1BH/snapshots_200crit_h329/h329.cosmo50PLK.3072gst5HbwK1BH.004096'}

keys = ['h148_10', 'h148_12', 'h148_249', 'h148_251', 'h148_27', 'h148_282', 'h148_3', 'h148_34', 'h148_38', 'h148_4', 'h148_55',
        'h148_6', 'h148_65', 'h229_14', 'h229_18', 'h229_20', 'h229_22', 'h229_49', 'h242_10', 'h242_21', 'h242_30', 'h242_38',
        'h242_401', 'h242_69', 'h242_8', 'h329_117', 'h329_29', 'h329_7']

# function that takes the filepath and processes necessary calculation
# large portion of this code was borrowed from DC_Justice_league code (bulkprocessing func)
def processing(filepath,sim,haloid,save=True):
    print('Running for simulation %s ' % filepath)

    # first, load the data
    s = pynbody.load(filepath)
    s.physical_units()
    h = s.halos(dummy=True)
    print('Loaded simulation')
    
    # we loop through all the halos, compute a value for that halo, and add it to the .data file
    X1 = h[1].properties['Xc']/s.properties['h']
    Y1 = h[1].properties['Yc']/s.properties['h']
    Z1 = h[1].properties['Zc']/s.properties['h'] # X,y,z coordinates in physical units

    # we load the copy of the halo to minimize computational stress
    halo = h.load_copy(haloid)
    halo.physical_units()

    # hostHalo property in order to determine which halo is the host of a satellite
    hostHalo = h[haloid].properties['hostHalo']

    if haloid==1:
            Xc = X1
            Yc = Y1
            Zc = Z1
    else:
            Xc = h[haloid].properties['Xc']/s.properties['h']
            Yc = h[haloid].properties['Yc']/s.properties['h']
            Zc = h[haloid].properties['Zc']/s.properties['h']


    # find the right properties for Navarro–Frenk–White (NFW) profile
    Msat = h[haloid].properties['mass']*(1.98847*10**30) # satellite mass in units of kg
    Rvir = (h[haloid].properties['Rvir']/s.properties['h'])*(3.08568*10**19) # Virial Radius and center coordinates, in units of m
    conct = h[haloid].properties['cNFW'] # concentration parameter
    Rs = Rvir/conct # scale radius
    rho0 = (Msat/(4*np.pi*Rs**3))*(1/(np.log(1+conct)-conct/(1+conct))) #density 0


    # save the outputs
    output = dict({
            'haloid': haloid,  # always put the haloid here
            'Rvir':Rvir,
            'Xc':Xc,
            'Yc':Yc,
            'Zc':Zc,
            'Msat': Msat,
            'conct': conct,
            'Rs': Rs,
            'rho0': rho0
            })

    print(f'> Returning {sim}_{haloid} outputs <')

    return output


def calc_snHeated(particles):
    """
    This function detects the gas particles that are sn-heated by comparing the coolontime 
    with the time 1 timestep before. Since the detection of sn-heating doesn't depend on any positional argument,
    this includes both particles being discharged and not.
    """
    #iterate detection process by pids
    pids = np.unique(particles['pid'])
    index = np.array([]) #initialize
    for pid in tqdm.tqdm(pids):
        data = particles[particles['pid']==pid]
        #create a structured array, containing index of dataframe, pid, time, and coolontime
        dtype = [('index', int), ('pid', int), ('time', float), ('coolontime', float)]
        structureArray=np.array(list(zip(data.index, *map(data.get, ['pid','time','coolontime']))), dtype=dtype)
        #limit to after being heated (avoid mistakingly take the row heated at the same timestep)
        heatedArray=structureArray[structureArray['time']>structureArray['coolontime']]
        #extract the list of unique coolontime, sorted by pid and time
        helper1, helper2 = np.unique(heatedArray['coolontime'], return_index = True)
        heatedunique = np.sort(heatedArray[helper2], order=['pid','time'])

        timebefore = heatedunique['time'][:-1]
        #find sn-heated list by comparing the time before and coolontime
        heatedLocal = heatedunique[1:][heatedunique['coolontime'][1:]>timebefore]
        indexLocal = heatedLocal['index'].astype(int)
        index = np.append(index, indexLocal)
    #based on detected indices, find the designated rows from original dataframe
    heated = particles[particles.index.isin(index)] 

    return heated