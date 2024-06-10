import pandas  as pd
import spaudiopy as spa
import numpy as np
import glob
from TS_TH_from_sphere_vector import TH_TS_wrapper
from TS_TH_from_sphere_vector import calc_TS_TH
from TS_TH_from_beamforming import energy_from_beamforming


def calc_TS_TH_decoder(ls_sig, tl, tu):
    # Berechnung der Richtungsenergien
    #front = sum(ls_sig[0, tl:tu])
    back = sum(ls_sig[5, tl:tu])
    top = sum(ls_sig[2, tl:tu])
    left = sum(ls_sig[1, tl:tu])
    right = sum(ls_sig[3, tl:tu])

    # TH - Top/Horizontal(left,right,back)
    TH = 20*np.log10((top)/(left + right + back))
    # TS - Top/Sides(left,right)
    TS = 20*np.log10((top)/(left + right))

    return TH, TS



def method_wrapper(method, path, start_milliseconds=15, stop_milliseconds=100, samplerate=44100):
    # get list of paths 
    HOAS_paths = sorted(glob.glob(path + "/*.wav"))
    # load HOAs from paths
    HOAS = spa.io.load_audio(HOAS_paths)

    # use method
    match method:
        case "beamforming":
            # calc energy/direction with Beamforming
            energy = energy_from_beamforming(HOAS.get_signals(), start_milliseconds=start_milliseconds, stop_milliseconds=stop_milliseconds, samplerate=samplerate)
            # calc parameters
            TH, TS = calc_TS_TH(energy)

        case "pseudo_intensity":
            # insert pseudo intensity function here

            B_format = spa.sig.AmbiBSignal.sh_to_b(spa.sig.MultiSignal(HOAS.get_signals()[0:4].tolist(), fs = 44100))
            azimuth, zenith, radius = spa.parsa.pseudo_intensity(B_format, win_len = 3, f_bp = (63, 8000))
            elevation = zenith - (np.pi / 2)
            TH, TS = TH_TS_wrapper(azimuth, elevation, radius, start_milliseconds=start_milliseconds, stop_milliseconds=stop_milliseconds, samplerate=samplerate)
        
        case "allrad_decoder":
            # definition of speaker set up
            ls_setup = spa.decoder.LoudspeakerSetup([1,0,0,0,0,-1], [0,1,0,-1,0,0], [0,0,1,0,-1,0])
            ls_setup.ambisonics_setup()
            # decoder signal
            ls_sig = spa.decoder.allrad(HOAS.get_signals(), ls_setup, 3)
            # calc paramter from directional energies
            TH, TS = calc_TS_TH_decoder(ls_sig, start_milliseconds, stop_milliseconds)
        
        case "allrad2_decoder":
            # definition of speaker set up
            ls_setup = spa.decoder.LoudspeakerSetup([1,0,0,0,0,-1], [0,1,0,-1,0,0], [0,0,1,0,-1,0])
            ls_setup.ambisonics_setup()
            # decoder signal
            ls_sig = spa.decoder.allrad2(HOAS.get_signals(), ls_setup, 3)
            # calc paramter from directionak energies
            TH, TS = calc_TS_TH_decoder(ls_sig, start_milliseconds, stop_milliseconds)
        
        case "mad_decoder":
            # definition of speaker set up
            ls_setup = spa.decoder.LoudspeakerSetup([1,0,0,0,0,-1], [0,1,0,-1,0,0], [0,0,1,0,-1,0])
            ls_setup.ambisonics_setup()
            # decoder signal
            ls_sig = spa.decoder.mad(HOAS.get_signals(), ls_setup, 3)
            # calc paramter from directionak energies
            TH, TS = calc_TS_TH_decoder(ls_sig, start_milliseconds, stop_milliseconds)
        
        case "reference":
            # insert reference
            weights = np.array(([500,-1,-1,720.1,-3.1,1.3,-1.3,-1.3,617.1],[503,0,723.1,0,-532.8,0,0,0,-311.2],[503,0,-723.1,0,-532.8,0,0,0,-311.2],[503,723.1,0,0,535.9,0,0,0,-305.8]))
            start_sample = int(start_milliseconds / 1000 * samplerate)
            stop_sample = int(stop_milliseconds /1000 * samplerate)
            ambi_3 = HOAS.get_signals()
            ambi_2 = ambi_3[[0,1,2,3,4,5,6,7,8]]
            ambi_2_sect = ambi_2[:,start_sample:stop_sample]
            ambi_2_sum = np.zeros(9)
            for i in range(9):
                ambi_2_sum[i] = np.sum(ambi_2_sect[i,:])
            tlbr_weights = ambi_2_sum * weights
            tlbr = np.zeros(4)
            for i in range(4):
                tlbr[i] = np.sum(tlbr_weights[i,:])
            TS = 10*np.log10((tlbr[0])**2/(tlbr[1] + tlbr[3])**2)
            TH = 10*np.log10((tlbr[0])**2/(tlbr[1] + tlbr[2] + tlbr[3])**2)
        
        case _:
            methods = ["beamforming", "pseudo_intensity", "allrad_decoder", "allrad2_decoder", "mad_decoder", "reference"]
            print("Unknown method. Methods are:")
            for m in methods:
               print(m)

            TS, TH = None, None
        
    return TS, TH
    


        

#def save_result():

#TS, TH = method_wrapper("allrad_decoder", "Raw Data/Applied Acoustics/Applied Acoustics/A10p/HOA")
#print(TS, TH)

 

