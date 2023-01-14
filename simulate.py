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

backLegSensorValues = numpy.zeros(100)
frontLegSensorValues = numpy.zeros(100)
# exit()

for i in range(100):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    time.sleep(0.02)

numpy.save(os.path.join('Data', 'backLegSensorValues'), backLegSensorValues)
numpy.save(os.path.join('Data', 'frontLegSensorValues'), frontLegSensorValues)

p.disconnect()
