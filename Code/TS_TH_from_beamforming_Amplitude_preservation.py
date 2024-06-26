'''
Script contains functions to calculcate Top Side and Top Horizontal from an Ambisonics signal with Beamforming.

Module inputs:
- data: Ambisonics signal in ACN channel ordering as np.ndarray
- N: Ambisonics order for calculation of TS and TH, N >= N of the Ambisonics signal
- pattern: Beamforming pattern, max_re, cardioid, hypercardioid
- start in milliseconds
- stop in milliseconds
- sample rate in Hz
- Fnm: ndarray with Ambisonics Filter function

Functions:
energy_from_beamforming: calcs energy/direction of an Ambisonics signal with Beamforming
plot_filter: plots spherical filters in 3d plot, based on spaudiopy plot.sh_coeffs definition

author:
avijah.sofie.neumann@campus.tu-berlin.de

date: 
03.06.2024

'''

import numpy as np
import spaudiopy as spa
import matplotlib.pyplot as plt
from matplotlib import cm, colors

def energy_from_beamforming(data: np.ndarray, N=2, pattern="hypercardioid", start_milliseconds=15, stop_milliseconds=100, samplerate=44100):
    # data: Ambisonics signal in ACN channel ordering

    # extracting relevant channels from signal
    x_nm = data[0:(N+1)**2,:]
    print(x_nm)
    # cutting signal
    start_sample = int(start_milliseconds / 1000 * samplerate)
    stop_sample = int(stop_milliseconds /1000 * samplerate)

    x_nm = x_nm[:,start_sample:stop_sample]

    # defining steering directions of the beampattern
    dirs = np.c_[[0,0],[0, np.pi/2],[np.pi/2,np.pi/2],[3*np.pi/2,np.pi/2],[np.pi, np.pi/2],[0,np.pi]]

    # getting beformer weights
    w_nm = spa.parsa.sh_beamformer_from_pattern(pattern, N,
                                          dirs[0,:], dirs[1,:]) #azi, zen
    
    # amplitude preservation after C. Hold, A. Politis, L. McCormack and V. Pulkki, "Spatial Filter Bank Design in the Spherical Harmonic Domain," 2021 29th European Signal Processing Conference (EUSIPCO), Dublin, Ireland, 2021, pp. 106-110, doi: 10.23919/EUSIPCO54536.2021.9616091.
    # load T-design for N+1
    sec_vecs = spa.grids.load_t_design(N+1)

    # convert cartesian coordinates into azimuth and elevation from the steering directions of the vector
    sec_azi, sec_zen, _ = spa.utils.cart2sph(*sec_vecs.T)

    # number of sectors
    J_sec = len(sec_vecs)

    # beampattern design
    c_n = spa.sph.hypercardioid_modal_weights(N)
    #c_n = spa.sph.maxre_modal_weights(N_sph_sec, True)  # works with amplitude compensation and without!

    # calculate matrix A for amplitude preservation
    A_sec = spa.sph.repeat_per_order(c_n) * \
            spa.sph.sh_matrix(N, sec_azi, sec_zen, 'real')

    delta_numSH = (N+1)**2 - (N+1)**2
    pw_secs = np.c_[A_sec, np.zeros([J_sec, delta_numSH])]

    #beamforming
    pw_secs_out = pw_secs @ x_nm
    pw_secs_out = np.real_if_close(pw_secs_out) 
    y = pw_secs_out
    
    # beamforming
    #y = spa.parsa.sh_beamform(w_nm, x_nm)

    # extract energys per direction
    top_energy = y[0,:]
    front_energy = y[1,:]
    left_energy = y[2,:]
    right_energy = y[3,:]
    back_energy = y[4,:]
    bottom_energy = y[5,:]

    energy = np.array([top_energy, front_energy, left_energy, right_energy, back_energy, bottom_energy])
    
    return energy

def plot_filter(F_nm, sh_type=None, azi_steps=5, el_steps=3, title=None,
              ax=None):
    # based on spaudiopy plot.sh_coeffs definition

    F_nm = spa.utils.asarray_1d(F_nm)
    F_nm = F_nm[:, np.newaxis]

    sh_type = 'complex' if np.iscomplexobj(F_nm) else 'real'

    theta_plot, phi_plot = np.meshgrid(np.linspace(0., 2 * np.pi,
                                        int(360 / azi_steps)),
                            np.linspace(10e-8, np.pi - 10e-8,
                                        int(180 / el_steps)))

    # inverse spherical harmonics transform to get the absolute value
    f_plot = spa.sph.inverse_sht(F_nm, theta_plot.ravel(), phi_plot.ravel(),
                    sh_type)
    f_r = np.abs(f_plot)

    if ax is None:
        fig = plt.figure(constrained_layout=True)
        ax = fig.add_subplot(projection='3d')
    else:
        fig = ax.get_figure()

    # define colormap
    m = cm.ScalarMappable(cmap=cm.jet,
                norm=colors.Normalize(vmin=0, vmax=1))
    m.set_array(f_r)
    c = m.to_rgba(f_r.reshape(theta_plot.shape))

    # surface plot
    ax.plot_surface(spa.utils.rad2deg(theta_plot), spa.utils.rad2deg(phi_plot),
        f_r.reshape(theta_plot.shape),
        facecolors=c,
        shade=False, linewidth=0.05, antialiased=True)
    
    ax.set_xlim(0,360)
    ax.set_ylim(0,180)
    ax.set_zlim(-0,1)

    ax.set_xticks([0,90,180,270,360])
    ax.set_yticks([0,90,180])
    ax.set_zticks([0,0.5,1])

    ax.set_xlabel(r'$\theta$' + r' (°)')
    ax.set_ylabel(r'$\phi$' + r' (°)') 
    ax.set_zlabel('S')

    ax.view_init(30, 60) # angle to show
    
    if title is not None:
        ax.set_title(title)

    plt.grid(True)