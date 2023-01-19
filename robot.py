import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT:
    def __init__(self):
        self.sensors={}
        self.motors={}
        
        self.robotId = p.loadURDF("body.urdf")
        
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK("brain.nndf")
        
        self.PrepareToSense()
        self.PrepareToAct()

    def PrepareToSense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self,t):
        for sens in self.sensors:
            self.sensors[sens].Get_Value(t)
    
    def PrepareToAct(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
    
    def Act(self, desiredAngle):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
                print(jointName, desiredAngle)
        # for motor in self.motors:
        #     self.motors[motor].Set_Value(self.robotId, desiredAngle)

    def Think(self):
        self.nn.Print()
        self.nn.Update()