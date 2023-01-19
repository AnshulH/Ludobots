import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        
        self.Prepare_To_Act()
    
    def Prepare_To_Act(self):
        self.amplitude = c.amplitudeBackLeg
        self.frequency = c.frequencyBackLeg
        self.offSet = c.phaseOffsetBackLeg
        
        if self.jointName == "Torso_BackLeg":
            self.frequency = self.frequency / 2

        self.motorValues = self.amplitude * numpy.sin(self.frequency * (numpy.linspace(0, (2*numpy.pi), 1000)) + self.offSet)

    def Set_Value(self, robotId, val):
        pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName=self.jointName, controlMode=p.POSITION_CONTROL, targetPosition=self.motorValues[val], maxForce=50)
    
    def Save_Values(self):
        numpy.save("data/motorValues.npy", self.motorValues)