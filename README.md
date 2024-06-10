# VAR-Project
TU Berlin: Virtual Acoustic Reality WS23/24: Project


# Introduction
This repository was developed as a student project for the course "Virtual Acoustic Reality" at TU Berlin. The aim is to calculate the 3D room acoustical parameters "Top Side" and "Top Down" using different methods. Currently, there is no unique way to calculate these room acoustic parameters. The goal of this project is to generate insights into these parameters and the methods used.

Successfully used methods are:

* beamforming
* pseudo intensity
* black box method from the paper [...]

# authors
avijah.sofie.neumann@campus.tu-berlin.de
linus.staubach@campus.tu-berlin.de
f.ulbricht@campus.tu-berlin.de

# How to install environment

* create python environment (tested on python 3.11)
* activate new environemnt
    * via terminal (open with str + ö) and conda: conda activate environemnt_name
    * check active environemnt via terminal with: conda info --env
* install python modules
    * via terminal: pip install -r .\requirements.txt
        * tipp: use TAB for auto complete path to double check
    * rerun command to check if modules were installed succesfully
    * run pip command every time requirements.txt is updated


# runnable scripts

* method_comparison.ipynb 
    * repository's main feature
    * compares Top Side / Top Horizontal paramters from different approaches
    * outputs plots and results in /out folder
* decoder_comparison.ipynb
    * compares ambisonic decoder from spaudiopy module
* plot_cube_to_sphere.py
    * run with Terminal prompt: "python .\Code\plot_cube_to_square.py"
    * plots and saves cube edges on sphere (as azimuth / elevation)


Date: 20.06.2024
