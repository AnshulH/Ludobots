import solution
import constants
import copy

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(0, constants.populationSize):
            self.parents.update({i: solution.SOLUTION(self.nextAvailableID)})
            self.nextAvailableID += 1

    def Evaluate(self, solutions):
        for i in solutions:
            solutions[i].Start_Simulation('DIRECT')

        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()


    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(constants.numberOfGenerations):
            if currentGeneration == 0:
                self.Evolve_For_One_Generation('GUI')
            else:
                self.Evolve_For_One_Generation('DIRECT')
        self.Show_Best()

    def Evolve_For_One_Generation(self, directOrGUI):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Mutate(self):
        for i in range(0, constants.populationSize):
            self.children[i].Mutate()

    def Print(self):
        print("\n")
        for i in range(0, constants.populationSize):
            print("Parent: %10f, \n Child: %10f" % (self.parents[i].fitness, self.children[i].fitness))
        print("\n")

    def Spawn(self):
        self.children = {}
        for i in range(0, constants.populationSize):
            self.children.update({i: copy.deepcopy(self.parents[i])})
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Select(self):
        for i in range(0, constants.populationSize):
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]

    def Show_Best(self):
        low = 5
        index = 0
        for idx in range(0, constants.populationSize):
            if self.parents[idx].fitness > low:
                low = self.parents[idx].fitness
                index = idx
        self.parents[index].Start_Simulation('GUI')