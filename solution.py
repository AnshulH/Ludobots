import os
import numpy
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = {}
        self.linkNames = []
        self.jointNames = []
        self.jointDirs = {
            0 : [0.5, 0.5, 0],
            1 : [-0.5, 0.5, 0],
            2 : [0, 0.5, 0.5]
        }
        self.linkDirs = {
            0 : [0.5, 0, 0],
            1 : [-0.5, 0, 0],
            2 : [0, 0, 0.5] 
        }
        self.relativeDirs = {
            0 : [1, 0, 0],
            1 : [-1, 0, 0],
            2 : [0, 0, 1] 
        }
    
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

        os.system('python3 simulate.py ' + directOrGUI + ' ' + str(self.myID) + ' 2&>1 &')
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def randomNum(self, left, right):
        return random.uniform(left, right)

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        totalLinks = 2
        zOldLink = numpy.array([self.randomNum(0.5, 1.5) for j in range(totalLinks)])

        xOldLink = self.randomNum(0.5, 1.5)
        yOldLink = self.randomNum(0.5, 1.5)

        pyrosim.Send_Cube(
            name = "Link0", 
            pos = [0, 0, zOldLink[0] / 2], 
            size = [xOldLink, yOldLink, zOldLink[0]], 
            color="Green")

        def flip(p):
            return True if random.random() < p else False

        for idx in range(1, totalLinks):  
            xSize = self.randomNum(0.5, 1.5)
            ySize = self.randomNum(0.5, 1.5)

            prevLinkname = "Link" +  str(idx-1)
            spawnLinkname = "Link" +  str(idx)

            yRelPosition = yOldLink
            zRelPosition = 0

            if idx== 1:
                yRelPosition = yOldLink / 2
                zRelPosition = numpy.max(zOldLink) / 2
            
            yOldLink = ySize

            pyrosim.Send_Joint(
                name = prevLinkname + "_" + spawnLinkname, 
                parent = prevLinkname, 
                child = spawnLinkname, 
                type = "revolute", 
                position = [0, yRelPosition, zRelPosition], 
                temp = "1 0 0")
            
            sensorType = flip(0.5)

            color = "Blue" if sensorType else "Green"

            if sensorType:
                self.linkNames.append(spawnLinkname)
                self.jointNames.append(prevLinkname + "_" + spawnLinkname)

            pyrosim.Send_Cube(name = spawnLinkname, pos = [0, ySize / 2, 0], size = [xSize, ySize, zOldLink[idx]], color=color)

            sizes = [xSize, ySize, zOldLink[idx]]
            for dir in range(0,3):
                self.randomCubes(dir, random.randint(0, 2), spawnLinkname, sizes)
                
        pyrosim.End()

    def randomCubes(self, direction, totalLinks, childName, sizes):
        linksize = [self.randomNum(0.5, 1), self.randomNum(0.5, 1), self.randomNum(0.5, 1)]
        oldLink = linksize 
        linkName = "Link" + str(direction)
        relativePosition = [sizes[0] * self.jointDirs[direction][0], sizes[1] * self.jointDirs[direction][1], sizes[2] * self.jointDirs[direction][2]]
        position = [linksize[0] * self.linkDirs[direction][0], linksize[1] * self.linkDirs[direction][1], linksize[2] * self.linkDirs[direction][2]]
        print(position)
        print(relativePosition)
            
        for link in range(totalLinks):
            if link == 0: 
                prevLinkname = childName
                xRange, yRange = sizes[0], sizes[1]
            else:
                relativePosition = [oldLink[0] * self.relativeDirs[direction][0], oldLink[1] * self.relativeDirs[direction][1], oldLink[2] * self.relativeDirs[direction][2]]
                prevLinkname = childName + linkName + str(link - 1)
                yRange = oldLink[1]
                xRange = oldLink[0]

            pyrosim.Send_Joint(name = prevLinkname + "_" + childName + linkName + str(link), 
                            parent = prevLinkname, child = childName + linkName + str(link), 
                            type = "revolute", 
                            position = relativePosition, 
                            temp = "1 0 0")

            sensorType = bool(random.getrandbits(1))

            color = "Blue" if sensorType else "Green"

            if sensorType:
                self.linkNames.append(childName + linkName + str(link))
                self.jointNames.append(prevLinkname + "_" + childName + linkName + str(link))

            if direction == 2:
                linksize[0] = min(linksize[0], xRange)

            pyrosim.Send_Cube(
                name = childName + linkName + str(link), 
                pos = position, 
                size = [linksize[0], min(linksize[1], yRange), linksize[2]], 
                color = color)

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        sensorcount = 0 
        # self.linkNames = ["Link0", "Link1", "Link1Link00", "Link1Link10", "Link1Link11", "Link1Link20"]
        # self.jointNames = ["Link0_Link1", "Link1_Link1Link00", "Link1_Link1Link10", "Link1Link10_Link1Link11", "Link1_Link1Link20"]
        while sensorcount < len(self.linkNames):
            pyrosim.Send_Sensor_Neuron(name = sensorcount, linkName = self.linkNames[sensorcount])
            sensorcount += 1
        
        idx=  0 
        motorcount = sensorcount + 1
        while idx < len(self.jointNames):
            pyrosim.Send_Motor_Neuron(name = motorcount, jointName = self.jointNames[idx])
            motorcount += 1
            idx += 1

        for currentRow in range(len(self.linkNames)):        
            for currentColumn in range(len(self.jointNames)):
                if (currentRow, currentColumn) not in self.weights:
                    self.weights[(currentRow, currentColumn)] = 4*random.random()
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + len(self.linkNames), weight = self.weights[(currentRow, currentColumn)])

        pyrosim.End()
    
    def Mutate(self):
        self.Mutate_Brain()

    def Mutate_Brain(self):
        allKeys = tuple(self.weights.keys())
        self.weights[allKeys[random.randint(0, len(allKeys)-1)]] = random.random() * 1 - 1
        
    def Set_ID(self, id):
        self.myID = id

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists('fitness' + str(self.myID) + '.txt'):
            time.sleep(0.01)
        
        fitnessFile = open('fitness' + str(self.myID) + '.txt', 'r')
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system('rm fitness' + str(self.myID) + '.txt')