'''
Script contains functions to calculcate Top Side and Top Horizontal from Azimuth, Zenith and Radius in a given time window.

Module inputs:
- azimuth as 1D array
- zenith as 1D array
- radius as 1D array
- start in milliseconds
- stop in milliseconds
- sample rate in Hz

Module contains subfunctions, which are all used in TH_TS_wrapper.

Functions:
y_top: calcs approximate line between middle and top sector
y_bottom: calcs approximate line between middle and bottom sector
sector_classifier: returns sector label for point in sphere
label2sectorname: takes label and returns sector name
add_sector2arrays: combines 1D input arrays and labels to one 2D array
energy_per_sector: calcs energy for each sector
calc_TS_TH: takes energy for each sector and return TS and TH
TH_TS_wrapper: wrapper function for whole module. Takes module inputs and returns TS and TH

author:
f.ulbricht@campus.tu-berlin.de

date: 
240520
'''


import numpy as np


def y_top(x, x_offset): 
    y_0_top = 0.6959132760153038  
    amplitude = 0.05408672398469633
    y_top = amplitude * np.sin((x-x_offset) * 2 * np.pi) + y_0_top

    return y_top



def y_bottom(x, x_offset):
    y_0_bottom = 0.3040867239846963
    amplitude = 0.05408672398469633
    y_bottom = -amplitude * np.sin((x-x_offset) * 2 * np.pi) + y_0_bottom

    return y_bottom



def sector_classfier(azi, zen):
    vertical_rigth_back = 0.75
    vertical_front_right = 0.25
    vertical_back_left = -0.75
    vertical_left_front = -0.25

    label = -1

    # back west
    if azi < vertical_back_left and azi >= -1:
        #check for top / bottom
        x_offset = -1.25

        # check top
        if zen > y_top(azi, x_offset):
            label = 0

        # check bottom
        elif zen < y_bottom(azi, x_offset):
            label = 5

        else:
            label = 4
            
    # left
    elif azi >= vertical_back_left and azi <= vertical_left_front:
        #check for top / bottom
        x_offset = -0.75

        # check top
        if zen > y_top(azi, x_offset):
            label = 0

        # check bottom
        elif zen < y_bottom(azi, x_offset):
            label = 5

        else:
            label = 2

    # front
    elif azi > vertical_left_front and azi < vertical_front_right:
        #check for top / bottom
        x_offset = -0.25

        # check top
        if zen > y_top(azi, x_offset):
            label = 0

        # check bottom
        elif zen < y_bottom(azi, x_offset):
            label = 5

        else:
            label = 1

    # right
    elif azi >= vertical_front_right and azi <= vertical_rigth_back:
        #check for top / bottom
        x_offset = 0.25

        # check top
        if zen > y_top(azi, x_offset):
            label = 0

        # check bottom
        elif zen < y_bottom(azi, x_offset):
            label = 5

        else:
            label = 3

    # back east
    elif azi > vertical_rigth_back and azi <= 1:
        #check for top / bottom
        x_offset = 0.75

        # check top
        if zen > y_top(azi, x_offset):
            label = 0

        # check bottom
        elif zen < y_bottom(azi, x_offset):
            label = 5

        else:
            label = 4


    return int(label)




def label2sectorname(label):    
    # give sectors a label
    match label:
        case 0:
            sector_name = "top"
        case 1:
            sector_name = "front"
        case 2:
            sector_name = "left"
        case 3:
            sector_name = "right"
        case 4:
            sector_name = "back"
        case 5:
            sector_name = "bottom"
        case _:
            sector_name = (f"could not determine sector name from label {label}")
    
    return sector_name



def add_sector2arrays(azimuth: np.ndarray, zenith: np.ndarray, radius: np.ndarray):
    
    data = np.empty((azimuth.shape[0], 4))
    for i, (azi_i, zen_i, r_i) in enumerate(zip(azimuth, zenith, radius)):
        label_i = sector_classfier(azi_i, zen_i)
        sample_data = np.array([azi_i, zen_i, r_i, label_i])
        data[i,:] = sample_data
        
    return data



def energy_per_sector(data: np.ndarray, start_milliseconds=15, stop_milliseconds=100, samplerate=44100):
    # data dimensions: azimuth, zeith, radius, label

    start_sample = int(start_milliseconds / 1000 * samplerate)
    stop_sample = int(stop_milliseconds /1000 * samplerate)

    data = data[start_sample:stop_sample, :]


    # get indices of label
    top_idx = np.where(data[:,3] == 0)[0]
    front_idx = np.where(data[:,3] == 1)[0]
    left_idx = np.where(data[:,3] == 2)[0]
    right_idx = np.where(data[:,3] == 3)[0]
    back_idx = np.where(data[:,3] == 4)[0]
    bottom_idx = np.where(data[:,3] == 5)[0]

    # sum energys per label
    top_energy = np.sum(data[[top_idx], 2])
    front_energy = np.sum(data[[front_idx], 2])
    left_energy = np.sum(data[[left_idx], 2])
    right_energy = np.sum(data[[right_idx], 2])
    back_energy = np.sum(data[[back_idx], 2])
    bottom_energy = np.sum(data[[bottom_idx], 2])

    energy = np.array([top_energy, front_energy, left_energy, right_energy, back_energy, bottom_energy])
    
    return energy




def calc_TS_TH(energy):
    TS = 10 * np.log10((energy[0] / (energy[2] + energy[3]))**2)
    TH = 10 * np.log10((energy[0] / (energy[2] + energy[3] + energy[4]))**2)

    return TS, TH


def TH_TS_wrapper(azimuth: np.ndarray, zenith: np.ndarray, radius: np.ndarray, start_milliseconds=15, stop_milliseconds=100, samplerate=44100):
    data = add_sector2arrays(azimuth, zenith, radius)
    energy = energy_per_sector(data, start_milliseconds=start_milliseconds, stop_milliseconds=stop_milliseconds, samplerate=samplerate)
    TH, TS = calc_TS_TH(energy)

    print("Top Horizontal:", TH)
    print("Top / Side:", TS)

    return TH, TS
