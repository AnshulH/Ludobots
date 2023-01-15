import pybullet as p
import pybullet_data
import time
import numpy
import pyrosim.pyrosim as pyrosim
import os

physicsClient = p.connect(p.GUI)

p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

amplitudeBackLeg = numpy.pi / 5
frequencyBackLeg = (numpy.pi * 4) / 90
phaseOffsetBackLeg = numpy.pi / 8

amplitudeFrontLeg = numpy.pi / 5
frequencyFrontLeg = (numpy.pi * 4) / 90
phaseOffsetFrontLeg = 0

backLegVal = numpy.zeros(1000)
frontLegVal = numpy.zeros(1000)

for i in range(1000):
    frontLegVal[i] = amplitudeFrontLeg * numpy.sin(frequencyFrontLeg*i + phaseOffsetFrontLeg)
    backLegVal[i] = amplitudeBackLeg * numpy.sin(frequencyBackLeg*i + phaseOffsetBackLeg)

for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_BackLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = backLegVal[i],
        maxForce = 90
    )
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_FrontLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = frontLegVal[i],
        maxForce = 90
    )
    time.sleep(1/240)

p.disconnect()
