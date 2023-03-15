import os
import numpy
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID, count):
        self.myID = nextAvailableID
        self.weights = {}
        self.linkNames = []
        self.jointNames = []
        self.created = False
        self.prevLinks = {}
        self.sizes = {}
        self.count = count
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

        os.system('python3 simulate.py ' + directOrGUI + ' ' + str(self.myID) + ' ' + str(self.count) + ' 2&>1 &')
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):
        if not self.created:
            pyrosim.Start_URDF("bodies0" + ".urdf")

            totalLinks = 2
            zOldLink = numpy.array([random.uniform(0.5, 1.5) for j in range(totalLinks)])

            xOldLink = random.uniform(0.5, 1.5)
            yOldLink = random.uniform(0.5, 1.5)

            self.prevLinks['xOldLink'] = xOldLink 
            self.prevLinks['yOldLink'] = yOldLink 
            self.prevLinks['zOldLink'] = zOldLink 

            pyrosim.Send_Cube(
                name = "Link0", 
                pos = [0, 0, zOldLink[0] / 2], 
                size = [xOldLink, yOldLink, zOldLink[0]], 
                color="Green")

            self.sizes['xSize'] = []
            self.sizes['ySize'] = []

            for i in range(1, totalLinks):  
                
                xSize = random.uniform(0.5, 1.5)
                ySize = random.uniform(0.5, 1.5)

                self.sizes['xSize'].append(xSize) 
                self.sizes['ySize'].append(ySize)

                parent_name = "Link" +  str(i - 1)
                child_name = "Link" +  str(i)

                if i == 1:
                    yRelPosition = yOldLink / 2
                    zRelPosition = numpy.max(zOldLink) / 2
                else:
                    yRelPosition = yOldLink
                    zRelPosition = 0
                
                yOldLink = ySize

                pyrosim.Send_Joint(
                    name = parent_name + "_" + child_name, 
                    parent = parent_name, 
                    child = child_name, 
                    type = "revolute", 
                    position = [0, yRelPosition, zRelPosition], temp = "1 0 0")

                sensorType = bool(random.getrandbits(1))

                color = "Blue" if sensorType else "Green"

                if sensorType:
                    self.linkNames.append(child_name)
                    self.jointNames.append(parent_name + "_" + child_name)

                pyrosim.Send_Cube(name = child_name, pos = [0, ySize / 2, 0], size = [xSize, ySize, zOldLink[i]], color=color)

                sizes = [xSize, ySize, zOldLink[i]]
                for dir in range(0,3):
                    self.childTotal = random.randint(0, 2)
                    self.randomCubes(dir, self.childTotal, child_name, sizes)
                    
            pyrosim.End()
            self.created = True
            self.count += 1
        else:
            pyrosim.Start_URDF("bodies" + str(self.count) + ".urdf")
            totalLinks = 2

            xOldLink = self.prevLinks['xOldLink'] 
            yOldLink = self.prevLinks['yOldLink'] 
            zOldLink = self.prevLinks['zOldLink'] 

            pyrosim.Send_Cube(
                name = "Link0", 
                pos = [0, 0, zOldLink[0] / 2], 
                size = [xOldLink, yOldLink, zOldLink[0]], 
                color="Green")

            for i in range(1, totalLinks):  
                
                xSize = self.sizes['xSize'][i-1]
                ySize = self.sizes['ySize'][i-1]

                parent_name = "Link" +  str(i - 1)
                child_name = "Link" +  str(i)

                if i == 1:
                    yRelPosition = yOldLink / 2
                    zRelPosition = numpy.max(zOldLink) / 2
                else:
                    yRelPosition = yOldLink
                    zRelPosition = 0
                
                yOldLink = ySize

                pyrosim.Send_Joint(
                    name = parent_name + "_" + child_name, 
                    parent = parent_name, 
                    child = child_name, 
                    type = "revolute", 
                    position = [0, yRelPosition, zRelPosition], temp = "1 0 0")

                sensorType = bool(random.getrandbits(1))

                color = "Blue" if sensorType else "Green"

                if sensorType:
                    self.linkNames.append(child_name)
                    self.jointNames.append(parent_name + "_" + child_name)

                pyrosim.Send_Cube(name = child_name, pos = [0, ySize / 2, 0], size = [xSize, ySize, zOldLink[i]], color=color)

                sizes = [xSize, ySize, zOldLink[i]]
                for dir in range(0,3):
                    self.randomCubes(dir, self.childTotal, child_name, sizes)
            self.count += 1
            pyrosim.End()
        # print(self.linkNames)


    def randomCubes(self, direction, totalLinks, childName, sizes):
        linksize = [random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1)]
        oldLink = linksize 
        linkName = "Link" + str(direction)
        relativePosition = [sizes[0] * self.jointDirs[direction][0], sizes[1] * self.jointDirs[direction][1], sizes[2] * self.jointDirs[direction][2]]
        position = [linksize[0] * self.linkDirs[direction][0], linksize[1] * self.linkDirs[direction][1], linksize[2] * self.linkDirs[direction][2]]
        print(position)
        print(relativePosition)
            
        for link in range(totalLinks):
            if link == 0: 
                parent_name = childName

                y_bound = sizes[1]
                x_bound = sizes[0]
            else:
                relativePosition = [oldLink[0] * self.relativeDirs[direction][0], oldLink[1] * self.relativeDirs[direction][1], oldLink[2] * self.relativeDirs[direction][2]]

                parent_name = childName + linkName + str(link - 1)

                y_bound = oldLink[1]
                x_bound = oldLink[0]

            pyrosim.Send_Joint(name = parent_name + "_" + childName + linkName + str(link), 
                            parent = parent_name, child = childName + linkName + str(link), 
                            type = "revolute", 
                            position = relativePosition, 
                            temp = "1 0 0")

            sensorType = bool(random.getrandbits(1))

            color = "Blue" if sensorType else "Green"

            if sensorType:
                self.linkNames.append(childName + linkName + str(link))
                self.jointNames.append(parent_name + "_" + childName + linkName + str(link))

            if direction == 2:
                linksize[0] = min(linksize[0], x_bound)

            pyrosim.Send_Cube(
                name = childName + linkName + str(link), 
                pos = position, 
                size = [linksize[0], min(linksize[1], y_bound), linksize[2]], 
                color = color)

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        sensorcount = 0 
        # self.linkNames = ["Link0", "Link1", "Link1Link00", "Link1Link10", "Link1Link11", "Link1Link20"]
        # self.jointNames = ["Link0_Link1", "Link1_Link1Link00", "Link1_Link1Link10", "Link1Link10_Link1Link11", "Link1_Link1Link20"]

        for id in self.linkNames:
            pyrosim.initLinkNames(id)

        while sensorcount < len(self.linkNames):
            pyrosim.Send_Sensor_Neuron(name = sensorcount, linkName = self.linkNames[sensorcount])
            sensorcount += 1
        
        i =  0 
        motorcount = sensorcount + 1
        while i < len(self.jointNames):
            pyrosim.Send_Motor_Neuron(name = motorcount, jointName = self.jointNames[i])
            motorcount += 1
            i += 1

        for currentRow in range(len(self.linkNames)):        
            for currentColumn in range(len(self.jointNames)):
                if (currentRow, currentColumn) not in self.weights:
                    self.weights[(currentRow, currentColumn)] = 4*random.random()
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + len(self.linkNames), weight = self.weights[(currentRow, currentColumn)])

        pyrosim.End()
    
    def biasedFlip(self):
        prob = 75
        val = random.randint(1,100)
        if val < prob:
            return 1
        return 0

    def Mutate(self):
        prob = self.biasedFlip()
        if prob == 1:
            self.Mutate_Brain()
        else:
            self.Mutate_Body()

    def Mutate_Brain(self):
        allKeys = tuple(self.weights.keys())
        self.weights[allKeys[random.randint(0, len(allKeys)-1)]] = random.random() * 1 - 1

    def Mutate_Body(self):
        self.sizes['xSize'][0] = random.uniform(0.5, 1.5)
        self.sizes['ySize'][0] = random.uniform(0.5, 1.5)
        
    def Set_ID(self, id):
        self.myID = id

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists('fitness' + str(self.myID) + '.txt'):
            time.sleep(0.01)
        
        fitnessFile = open('fitness' + str(self.myID) + '.txt', 'r')
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system('rm fitness' + str(self.myID) + '.txt')