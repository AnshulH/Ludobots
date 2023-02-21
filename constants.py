

import numpy as numpy
import random
pi_four = numpy.pi / 4.0

num_iterations = 1000
time_step = 1/1000 #60

max_force = 200
amplitude = pi_four
frequency = 10
offset = numpy.pi / 8.0

numberOfGenerations = 10 #10
populationSize = 1 # 10

numLinks = 4
numSensorNeurons = 3 
numMotorNeurons = numSensorNeurons - 1 
sensors = []
for i in range(numSensorNeurons):
    r = random.randint(0, numLinks)
    sensors.append(r)
motorJointRange = 0.3