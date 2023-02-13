import os
import numpy
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID

        self.linkNames = []
        self.jointNames = []
    
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system('python3 simulate.py ' + directOrGUI + ' ' + str(self.myID) + ' 2&>1 &')
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-5, 0, 0.25], size=[1, 1, 0.5])
        pyrosim.End()

    def Create_Body(self):
        self.linkNames = []
        self.jointNames = []

        pyrosim.Start_URDF("body.urdf")

        num_links = numpy.random.randint(3, 9)
        zLen = numpy.random.uniform(0.5, 1.5, num_links + 1)

        xLink = numpy.random.uniform(0.5, 1.5)
        yLink = numpy.random.uniform(0.5, 1.5)

        pyrosim.Send_Cube(
            name="Link0",
            pos=[0, 0, zLen[0] / 2],
            size=[xLink, yLink, zLen[0]],
            color=False
        )

        for i in range(1, num_links):  
            xSize = numpy.random.uniform(0.5, 1.5)
            ySize = numpy.random.uniform(0.5, 1.5)

            parent_name = "Link" + str(i - 1)
            child_name = "Link" + str(i)

            if i == 1:
                yLoc = yLink / 2
                zLoc = numpy.max(zLen) / 2
            else:
                yLoc = yLink
                zLoc = 0
            
            yLink = ySize

            pyrosim.Send_Joint(
                name=parent_name + "_" + child_name,
                parent=parent_name,
                child=child_name,
                type="revolute",
                position=[0, yLoc, zLoc],
                jointAxis="1 0 0"
            )
            
            color = bool(numpy.random.randint(0, 2))

            if color:
                self.linkNames.append(child_name)
                self.jointNames.append(parent_name + "_" + child_name)

            pyrosim.Send_Cube(
                name=child_name,
                pos=[0, ySize / 2, 0],
                size=[xSize, ySize, zLen[i]],
                color=color
            )
        
        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        sensorcount = 0 
        for link_name in self.linkNames:
            pyrosim.Send_Sensor_Neuron(sensorcount, link_name)
            sensorcount += 1

        motorcount = sensorcount
        for i, joint_name in enumerate(self.jointNames):
            pyrosim.Send_Motor_Neuron(motorcount, joint_name)
            motorcount += 1

        for i, link_name in enumerate(self.linkNames):        
            for j, joint_name in enumerate(self.jointNames):
                pyrosim.Send_Synapse(i, j + len(self.linkNames), 1.0)

        pyrosim.End()

    def Set_ID(self, id):
        self.myID = id

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists('fitness' + str(self.myID) + '.txt'):
            time.sleep(0.01)
        
        fitnessFile = open('fitness' + str(self.myID) + '.txt', 'r')
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system('rm fitness' + str(self.myID) + '.txt')