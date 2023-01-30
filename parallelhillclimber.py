from solution import SOLUTION
import constants as c
import copy

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        self.nextAvailableID = 0
        self.parents = {}
        for val in range(0, c.populationSize):
            self.parents[val] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        # print(self.parents)

    def EVOLVE(self):

        for i in range(0, len(self.parents)):
            self.parents[i].Start_Simulation('DIRECT')

        for i in range(0, len(self.parents)):
            self.parents[i].Wait_For_Simulation_To_End()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}

        for i in range(len(self.parents)):
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in range(len(self.children)):
            self.children[i].Mutate()

    def Select(self):
        for i in range(len(self.parents)):
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]

    def Print(self):
        for key in self.parents.keys():
            print('\nParent fitness: ', self.parents[key].fitness, ', child fitness: ', self.children[key].fitness)

    def Show_Best(self):
        min_fitness = self.parents[0].fitness
        for i in range(len(self.parents)):
            min_fitness = min(self.parents[i].fitness, min_fitness)
        
        for i in range(len(self.parents)):
            if self.parents[i].fitness == min_fitness:
                self.parents[i].Start_Simulation('GUI')

