# import pybullet as p
# import pyrosim.pyrosim as pyrosim
# from sensor import SENSOR
# from motor import MOTOR
# import os
# from pyrosim.neuralNetwork import NEURAL_NETWORK

# class ROBOT:
#     def __init__(self, solutionId):
#         self.sensors = {}
#         self.motors = {}

#         self.myId = solutionId
#         self.robotId = p.loadURDF("body.urdf")
        
#         pyrosim.Prepare_To_Simulate(self.robotId)
#         self.nn = NEURAL_NETWORK("brain" + str(self.myId) + ".nndf")
        
#         self.PrepareToSense()
#         self.PrepareToAct()
#         os.system("rm " "brain" + str(self.myId) + ".nndf")

#     def PrepareToSense(self):
#         for linkName in pyrosim.linkNamesToIndices:
#             self.sensors[linkName] = SENSOR(linkName)
    
#     def Sense(self, t):
#         for sens in self.sensors:
#             self.sensors[sens].Get_Value(t)
    
#     def PrepareToAct(self):
#         for jointName in pyrosim.jointNamesToIndices:
#             self.motors[jointName] = MOTOR(jointName)
    
#     def Act(self, desiredAngle):
#         for neuronName in self.nn.Get_Neuron_Names():
#             if self.nn.Is_Motor_Neuron(neuronName):
#                 jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
#                 desiredAngle = self.nn.Get_Value_Of(neuronName)
#                 self.motors[jointName].Set_Value(self.robotId, desiredAngle)

#     def Get_Fitness(self):
#         stateOfLinkZero = p.getLinkState(self.robotId,0)
#         positionOfLinkZero = stateOfLinkZero[0]
#         xCoordinateOfLinkZero = positionOfLinkZero[0]
#         fitness_path = "tmp" + str(self.myId) + ".txt"
#         with open(fitness_path, 'w') as out_file:
#             out_file.write(str(xCoordinateOfLinkZero))

#         os.system(f"mv tmp{self.myId}.txt fitness{self.myId}.txt")

#     def Think(self):
#         self.nn.Update()

import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self, solutionID):
        self.sensors = {}
        self.motors = {}
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        self.robotId = p.loadURDF(f"body{solutionID}.urdf")
        self.solutionId = solutionID
        os.system(f"rm brain{solutionID}.nndf")
        os.system(f"rm body{solutionID}.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for linkName, sensor in self.sensors.items():
            sensor.Get_Value(t)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)    
                desiredAngle = self.nn.Get_Value_Of(neuronName)   
                self.motors[jointName].Set_Value(desiredAngle, self.robotId)

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId,0)        
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        print(xCoordinateOfLinkZero)

        fit_file = open(f"tmp{self.solutionId}.txt", "w")
        fit_file.write(str(xCoordinateOfLinkZero))

        os.system(f"mv tmp{self.solutionId}.txt fitness{self.solutionId}.txt")
   
    def Think(self):
        self.nn.Update()
