import pybullet as p
import pybullet_data

class WORLD:
    def __init__(self, dOrG):
        print(dOrG)
        if dOrG == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        
        self.planeId = p.loadURDF("plane.urdf")
        p.loadSDF("world.sdf")