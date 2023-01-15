import pybullet as p
import pybullet_data
import time
import numpy
import pyrosim.pyrosim as pyrosim
import os
import constants as c
from simulation import SIMULATION

simulation = SIMULATION()
simulation.Run()
# simulation.Run()
# physicsClient = p.connect(p.GUI)

# p.setAdditionalSearchPath(pybullet_data.getDataPath())
# p.setGravity(0,0,-9.8)
# planeId = p.loadURDF("plane.urdf")
# robotId = p.loadURDF("body.urdf")
# p.loadSDF("world.sdf")

# pyrosim.Prepare_To_Simulate(robotId)

# for i in range(1000):
#     c.frontLegVal[i] = c.amplitudeFrontLeg * numpy.sin(c.frequencyFrontLeg*i + c.phaseOffsetFrontLeg)
#     c.backLegVal[i] = c.amplitudeBackLeg * numpy.sin(c.frequencyBackLeg*i + c.phaseOffsetBackLeg)

# for i in range(1000):
#     p.stepSimulation()
#     c.backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
#     c.frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
#     pyrosim.Set_Motor_For_Joint(
#         bodyIndex = robotId,
#         jointName = "Torso_BackLeg",
#         controlMode = p.POSITION_CONTROL,
#         targetPosition = c.backLegVal[i],
#         maxForce = 90
#     )
#     pyrosim.Set_Motor_For_Joint(
#         bodyIndex = robotId,
#         jointName = "Torso_FrontLeg",
#         controlMode = p.POSITION_CONTROL,
#         targetPosition = c.frontLegVal[i],
#         maxForce = 90
#     )
#     time.sleep(1/240)

# p.disconnect()
