import os
import sys
import logging


class Loci():
    chromsome = "init"
    strand = '+'
    start_pos = 0
    end_pos = 0
    get_length = 0

class Structure():
    position = Loci()

    free_energy = 0.0
    gsigma=0.0
    bp_energy = 0.0
    boltzmann_factor = 0.0
    probability = 0.0
    residual_twist = 0.0
    current_Gsigma = 0.0
    external = False
    external_length = 0

