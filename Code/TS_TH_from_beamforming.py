'''
Script contains functions to calculcate Top Side and Top Horizontal from an Ambisonics signal.

Module inputs:
- data: Ambisonics signal in ACN channel ordering as np.ndarray
- Ambisonics order for calculation of TS and TH, N >= N of the Ambisonics signal
- start in milliseconds
- stop in milliseconds
- sample rate in Hz


Functions:
energy_from_beamforming: calcs energy/direction of an Ambisonics signal with Beamforming


author:


date: 
03.06.2024

'''

import numpy as np
import spaudiopy as spa


def energy_from_beamforming(data: np.ndarray, start_milliseconds=15, stop_milliseconds=100, samplerate=44100):
    # data: Ambisonics signal in ACN channel ordering

    N=2

    # extracting relevant channels from signal
    x_nm = data[0:(N+1)**2,:]
    
    # cutting signal
    start_sample = int(start_milliseconds / 1000 * samplerate)
    stop_sample = int(stop_milliseconds /1000 * samplerate)

    data = data[start_sample:stop_sample, :]

    # defining steering directions of the beampattern
    vec = np.array([[0,0,1],[1,0,0],[0,-1,0],[0,1,0],[-1,0,0],[0,0,-1]]) #top, front, left, right, back, bottom

    # conversion of vec: [x,y,z] to dir: [azi, zen]
    dirs = spa.utils.vec2dir(vec)

    # getting beformer weights
    w_nm = spa.parsa.sh_beamformer_from_pattern('max_rE', N,
                                          dirs[:,0], dirs[:,1]) #azi, zen
    
    # beamforming
    y = spa.parsa.sh_beamform(w_nm, x_nm)

    # sum energys per direction
    top_energy = np.sum(y[0,:])
    front_energy = np.sum(y[1,:])
    left_energy = np.sum(y[2,:])
    right_energy = np.sum(y[3,:])
    back_energy = np.sum(y[4,:])
    bottom_energy = np.sum(y[5,:])

    energy = np.array([top_energy, front_energy, left_energy, right_energy, back_energy, bottom_energy])
    
    return energy