import pybullet as p
import pyrosim.pyrosim as pyrosim
import os

from sensor import SENSOR
from motor import MOTOR
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.robotId = p.loadURDF("bodies0"+ ".urdf")

        pyrosim.Prepare_To_Simulate(self.robotId)

        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        self.nn = NEURAL_NETWORK("brain" + str(self.solutionID) + ".nndf")

        os.system('rm brain' + str(self.solutionID) + '.nndf')
    
    def Prepare_To_Sense(self):
        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self, t):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(t)
        
    def Prepare_To_Act(self):
        self.motors = {} 

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
    
    def Act(self, t, robot):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                if jointName not in self.motors:
                    self.motors[jointName] = MOTOR(jointName)
                motor = self.motors[jointName]
                motor.Set_Value(desiredAngle, robot, self.robotId)
        
    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        yPosition = basePositionAndOrientation[0][1]

        f = open('tmp' + str(self.solutionID) + '.txt', 'w')
        f.write(str(yPosition))
        f.close()
        os.system('mv tmp' + str(self.solutionID) + '.txt fitness' + str(self.solutionID) + '.txt') 
        

