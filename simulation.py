import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import time

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self, dOrG, solutionID):
        self.world = WORLD(dOrG)
        self.robot = ROBOT(solutionID)

    def Run(self):
        for i in range(1000):
            p.stepSimulation()

            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            self.robot.Get_Fitness()

            time.sleep(1/2400)

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()