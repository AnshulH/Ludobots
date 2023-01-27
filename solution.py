import numpy 
import pyrosim.pyrosim as pyrosim
import random
import os

class SOLUTION:
    def __init__(self):
        self.weights = 2 * numpy.random.rand(3, 2) - 1

    def Evaluate(self, dOrG = "DIRECT"):
        # os.system("python3 simulate.py")
        self.Generate_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system(f"python3 simulate.py {str(dOrG)}")

        with open('fitness.txt', 'r') as in_file:
            self.fitness = float(in_file.readlines()[0])

    def Mutate(self):
        row, col = self.weights.shape
        self.weights[random.randint(0, row-1), random.randint(0, col-1)] = 2 * random.random() - 1

    def Generate_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[(-3),(2),(0.5)], size=[(1),(1),(1)])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[(1),(0),(1.5)], size=[(1),(1),(1)])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[(0.5),(0),(1)])
        pyrosim.Send_Cube(name="BackLeg", pos=[(-0.5),(0),(-0.5)], size=[(1),(1),(1)])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[(1.5),(0),(1)])
        pyrosim.Send_Cube(name="FrontLeg", pos=[(0.5),(0),(-0.5)], size=[(1),(1),(1)])
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 4 , jointName = "Torso_FrontLeg")

        for currentRow in [0, 1, 2]:
            for currentColumn in [0, 1]:
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + 3, weight = self.weights[currentRow][currentColumn])
        pyrosim.End()
