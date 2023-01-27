import pybullet as p
import pybullet_data
import time
import numpy
import pyrosim.pyrosim as pyrosim
import os
import constants as c
import sys
from simulation import SIMULATION

dOrG = sys.argv[1]

simulation = SIMULATION(dOrG)
simulation.Run()
simulation.Get_Fitness()