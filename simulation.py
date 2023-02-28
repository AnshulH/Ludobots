from world import WORLD
from robot import ROBOT

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import constants as c
import time as time

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT) 
        else:
            self.physicsClient = p.connect(p.GUI) 
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        p.setGravity(0, 0, -9.8)

        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def run(self):
        for i in range(c.num_iterations):
            p.stepSimulation()

            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i, self.robot)

            if self.directOrGUI == 'GUI':
                time.sleep(c.time_step)

    def __del__(self):
        p.disconnect()
    
    def Get_Fitness(self):
        self.robot.Get_Fitness()

        
        
        

        