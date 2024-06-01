import pandas  as pd
import spaudiopy as spa
import numpy as np
import glob
from TS_TH_from_sphere_vector import TH_TS_wrapper


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
    HOAS_paths = glob.glob(path + "/*.wav")
    # load HOAs from paths
    HOAS = spa.io.load_audio(HOAS_paths)

    # use method
    match method:
        case "beamforming":
            # insert beamformer function here
            TH, TS = 0, 0

        case "pseudo_intensity":
            # insert ppseudo intensity function here
            azimuth = 0
            zenith = 0
            radius = 0
            
            TH, TS = TH_TS_wrapper(azimuth, zenith, radius, start_milliseconds=start_milliseconds, stop_milliseconds=stop_milliseconds, samplerate=samplerate)
        
        case "allrad_decoder":
            # definition of speaker set up
            ls_setup = spa.decoder.LoudspeakerSetup([1,0,0,0,0,-1], [0,1,0,-1,0,0], [0,0,1,0,-1,0])
            ls_setup.ambisonics_setup()
            # decoder signal
            ls_sig = spa.decoder.allrad(HOAS.get_signals(), ls_setup, 3)
            # calc paramter from directionak energies
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
        
        case _:
            methods = ["beamforming", "pseudo_intensity", "allrad_decoder", "allrad2_decoder", "mad_decoder"]
            print("Unknown method. Methods are:")
            for m in methods:
               print(m)

            TS, TH = None, None
        
    return TS, TH
    


        

#def save_result():

#TS, TH = method_wrapper("allrad_decoder", "Raw Data/Applied Acoustics/Applied Acoustics/A10p/HOA")
#print(TS, TH)

 

