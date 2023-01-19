import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import time

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self):
        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        for i in range(1000):
            p.stepSimulation()

            self.robot.Sense(i)
            self.robot.Act(i)
            self.robot.Think()

            time.sleep(1/240)

    def __del__(self):
        p.disconnect()