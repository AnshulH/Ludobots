# Main executable, run to simulate as many generations and trials as specified in constants.py

import os
import parallelhillclimber

os.system('rm brain*.nndf')
os.system('rm fitness*.txt')
phc = parallelhillclimber.PARALLEL_HILL_CLIMBER()
phc.Evolve()