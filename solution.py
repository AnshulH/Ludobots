import os
import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.lengths = {}
        self.jointNames = {}
        self.spawns = {}
        self.dirs = {
            0: [1,0,0],
            1: [-1,0,0],
            2: [0,1,0],
            3: [0,-1,0],
            4: [0,0,1]
        }

        self.coordDirs = {
            0: {
                0: [0,0,0],
                1: [-1, 0, 0],
                2: [-0.5,-0.5,0],
                3: [0,-0.5,0.5],
                4: [0.5,0,0.5],
            },
            1: {
                0: [-1,0,0],
                1: [0, 0, 0],
                2: [-0.5,-0.5,0],
                3: [0,-0.5,0.5],
                4: [0.5,0,0.5],
            },
            2: {
                0: [-0.5,-0.5,0],
                1: [0,-0.5,0.5],
                2: [0,0,0],
                3: [0,-1,0],
                4: [0.5,0,0.5],
            },
            3: {
                0: [-0.5,-0.5,0],
                1: [0,-0.5,0.5],
                2: [0,-1,0],
                3: [0,0,0],
                4: [0.5,0,0.5],
            },
            4 : {
                0: [-0.5,-0.5,0],
                1: [0,-0.5,0.5],
                2: [0.5,0.5,0],
                3: [0,0.5,0.5],
                4: [0.5,0,0.5],
            }   
        }
        
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons) * 2 - 1

    def Evaluate(self, directOrGUI):
        self.Create_Body()
        self.Create_Brain(self.myID)
        self.Create_World()
        directOrGUI = "GUI"
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " &")
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        print(self.fitness)
        f.close()
    
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system('python3 simulate.py ' + directOrGUI + ' ' + str(self.myID) + ' &')
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-5, 0, 0.25], size=[1, 1, 0.5])
        pyrosim.End()

    def Create_Body(self):

        pyrosim.Start_URDF("body.urdf")

        num_links = c.numLinks
        childCoords = {}
        curr = None

        for linkNum in range(0, num_links):  
            linkName = "Link{}".format(linkNum)
            self.lengths[linkNum] = np.random.rand(3,1)
            if (linkNum == 0):
                # Absolute positioning
                pyrosim.Send_Cube(name=linkName, pos=[0, 0, 0], size=self.lengths[linkNum], color="Blue")
                currDir = self.dirs[np.random.randint(0, 4)]
                childCoords[linkNum] = [currDir[0]*0.5, currDir[1]*0.5, currDir[2]*0.5]
            else:    
                coordinate = np.random.randint(0, 4) if curr == None else currCoord
                currCoord = np.random.randint(0, 4)
                currDir = self.dirs[currCoord]
                pyrosim.Send_Cube(
                    name=linkName, 
                    pos=[currDir[0]/2, currDir[1]/2, currDir[2]/2], 
                    size=self.lengths[linkNum], 
                    color="Green")
                if coordinate != currCoord:
                    childCoords[linkNum] = [self.lengths[linkNum][0], 0, 0]
                elif coordinate == currCoord - 1:
                    childCoords[linkNum] = [0, 0, 0]
                    # choose side to add to
        # 1 x 2 -x 3 y 4 -y 5 +z
                else:
                    childCoords[linkNum] = [self.coordDirs[coordinate][currCoord][0], self.coordDirs[coordinate][currCoord][1], self.coordDirs[coordinate][currCoord][2]]

            if linkNum in self.spawns:
                self.spawns[linkNum].append(linkNum+1)
            else:
                self.spawns[linkNum] = [linkNum+1]

            if linkNum == num_links - 1:
                break
            jointVal = " ".join(str(random.random()) for _ in range(3))
            pyrosim.Send_Joint(
                name = f"Link{linkNum}_Link{linkNum+1}", 
                parent = linkName, 
                child = "Link{}".format(linkNum+1), 
                type = "revolute", 
                position= childCoords[linkNum], 
                jointAxis = jointVal)

        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        count = 0

        for idx in range(c.numLinks):
            if idx in c.sensors:
                pyrosim.Send_Sensor_Neuron(name=count, linkName=f"Link{idx}")
        
                if idx == c.numLinks - 1 or idx not in self.spawns:
                    continue
            
                for kid in self.spawns[idx]:
                    joint_name = f"Link{idx}_Link{kid}"
                    pyrosim.Send_Motor_Neuron(name=count, jointName=joint_name)
                    count += 1

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, 
                targetNeuronName = currentColumn + c.numSensorNeurons, 
                weight = self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Set_ID(self, id):
        self.myID = id

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.0001)
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        f.close
        os.system("rm" + " fitness" + str(self.myID) + ".txt")

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons -1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow,randomColumn] = random.random() * 2 - 1