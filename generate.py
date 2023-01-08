import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

for x in range(0, 5):
    for y in range(0, 5):
        z = 0.5
        for dir in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[(0.9**dir), (0.9**dir), (0.9**dir)])
            z += 1

pyrosim.End()