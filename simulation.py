import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import time

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy
import math
from world import WORLD
from robot import ROBOT
from sensor import SENSOR

class SIMULATION:
    def __init__(self, directOrGUI="GUI", solutionID=0):
        directOrGUI = "GUI"
        # if directOrGUI == "DIRECT":
        #     self.physicsClient = p.connect(p.DIRECT)
        # else:
        self.physicsClient = p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        # p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.robot = ROBOT(solutionID)

    def Get_Fitness(self, solutionID):
        self.robot.Get_Fitness(solutionID)

    def Run(self):
        for i in range(500):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i, self.robot.robotId)
            time.sleep(1/100)

    def __del__(self):
        p.disconnect()