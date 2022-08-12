import random
from time import sleep
import numpy as np
from regex import E
import json
from Components.NeuralNetwork import NeuralNetwork


class AlgorithmGenetic:
    def __init__(self,Npop,layers):
        self.Npop = Npop
        self.Pop = []
        self.Prcr = 0.7
        self.Prmut = 0.01
        self.best = []
        self.LayerArchitecture = layers
        self.lastMaxScore = 0
        # 8 bit . 52 bit on one weight
        # 180 bits on all

    def restartAll(self):
        for pop in self.Pop:
            pop[1] = 0
    def createPopulation(self,GetOldPop):
        #FILL THE MATRIX WITH NEURAL NETWORK
        OldPop = []
        if GetOldPop:
            files = open("data.txt", "r")
            for line in files:
                OldPop.append(json.loads(line[:-1]))
            files.close()  
            if self.Npop != len(OldPop):
                for i in range(self.Npop):
                    self.Pop.append([NeuralNetwork(self.LayerArchitecture,3),0])
            else:
                for i in range(len(OldPop)):
                    self.Pop.append([NeuralNetwork(self.LayerArchitecture,3),0])
                    self.Pop[i][0].changeWeight(OldPop[i])

        else:
            for i in range(self.Npop):
                self.Pop.append([NeuralNetwork(self.LayerArchitecture,3),0])

    def Save(self):
        files = open("data.txt", "w")
        for Pop in self.Pop:
            files.write(str(Pop[0].getWeight()) + "\n")
        files.close()

    def restartScore(self):
        for i in range(self.Npop):
            self.Pop[i][1] = -1

    def GetBest(self):
        best = [0,0]
        for i in range(len(self.Pop)):
            if self.Pop[i][1] > best[1]:
                best = [i,self.Pop[i][1]]
        return best
            
    def setScore(self,index,score):
        self.Pop[index][1] = score
            
    def ChangeNNWeight(self):
        # ErrorList = []
        # for Pop in self.Pop:
        #     getData = Pop[0].GetLastData()
        #     if getData[0][0] > getData[0][1]:
        #         getData[1][0] = 1
        #     else:
        #         getData[1][0] = 0
        #     # if getData[1][0] >= 0.5:
        #     #     getData[1][0] -= 0.5
        #     # else:
        #     #     getData[1][0] += 0.5
        #     getData[1][1] = random.uniform(0,1)
            
        #     ErrorList.append(getData)
        
        

        self.chooseCrossover()
        self.CrossOver()
        self.Motation()

        # for Pop in self.Pop:
        #     Pop[0].Supervised(ErrorList,10)

        self.Save()

    def chooseCrossover(self):
        sum = 0
        pdf = []
        cdf = []
        self.CrossOvers = []
        #calc the sum
        for Pop in self.Pop:
            sum += Pop[len(Pop) - 1]
        if sum == 0:
            for i in range(int(self.Npop / 2)):
                self.CrossOvers.append([random.randint(0,self.Npop - 1),random.randint(0,self.Npop - 1)])
        else:
            #calc the cdf MEAN THE PROBABILITY OF EVERY POPULATION
            GenerationMaxScore = self.GetBest()
            MaxScoreList = []
            for i in range(len(self.Pop)):
                if self.Pop[i][1] == GenerationMaxScore[1]:
                    MaxScoreList.append(i)
            if GenerationMaxScore[1] >= self.lastMaxScore and len(MaxScoreList) <= int(self.Npop / 3):
                for i in range(int(self.Npop / 2)):
                    self.CrossOvers.append([random.choice(MaxScoreList),random.choice(MaxScoreList)])
                
            else:
                for Index,Pop in enumerate(self.Pop):
                    Dividation = Pop[len(Pop) - 1] / sum
                    pdf.append(Dividation)
                    if Index != 0 : cdf.append(cdf[Index - 1] + (Dividation))
                    elif Index == self.Npop - 1 : cdf.append(1)
                    else: cdf.append(Dividation)
                #Crossover between POPULATION work by cdf
                for CrossOver in range(int(self.Npop / 2)):
                    Parent = []
                    while len(Parent) != 2:
                        Parent = []
                        while len(Parent) != 2:
                            Lower = 0
                            prob = random.uniform(0,1)
                            for Index,Upper in enumerate(cdf):
                                if Lower < prob <= Upper:
                                    Parent.append(Index)
                                    break
                                Lower = Upper
                    self.CrossOvers.append(Parent)
            self.lastMaxScore = GenerationMaxScore[1]
        
        # # self.chooseBest(2)    
        # self.Pop.sort(key=lambda x: x[1])
        # for i in range(len(self.CrossOvers)):
        #     self.CrossOvers[i] = [self.Npop - 1,self.Npop - 2]
    
    def CrossOver(self):
        Pop = []
        #crossover
        for Crossover in self.CrossOvers:
            prob = random.uniform(0,1)
            
            if prob <= self.Prcr:
                FirstPop = self.Pop[Crossover[0]][0].getWeight()
                SecondPop = self.Pop[Crossover[1]][0].getWeight()

                for i in range(len(FirstPop)):
                    prob = random.uniform(0,1)
                    if prob <= 0.5:
                        Chromosome1 = FirstPop[i]
                        Chromosome2 = SecondPop[i]
                        for j in range(len(Chromosome1)):
                            Chromosome1[j],Chromosome2[j] = self.ChromosomeSwap(Chromosome1[j],Chromosome2[j])

                SELF_FBRAIN = NeuralNetwork(self.LayerArchitecture,3)
                SELF_SBRAIN = NeuralNetwork(self.LayerArchitecture,3)

                SELF_FBRAIN.changeWeight(FirstPop)
                SELF_SBRAIN.changeWeight(SecondPop)

                Pop.append([SELF_FBRAIN,0])
                Pop.append([SELF_SBRAIN,0])

            else:
                #if random number bigger tha Prcr than this mean we clone the population
                Pop.append(self.Pop[Crossover[0]])
                Pop.append(self.Pop[Crossover[1]])
        #to make sure the number of pup is the same
        if len(Pop) != self.Npop:Pop.append(self.Pop[random.randint(0,self.Npop - 1)])
        self.Pop = Pop
    
    def Motation(self):
        #motation have little possibility we do it to make sure the Algorithme not stuck in Desired value
        for Pop in self.Pop:
            prob = random.uniform(0,1)
            if prob < self.Prmut: 
                Weight = Pop[0].getWeight()
                for i in range(len(Weight)):
                    prob = random.uniform(0,1)
                    if prob <= 0.5:
                        Weight[i] = np.random.randn()

    def ChromosomeSwap(self,Chromosome1,Chromosome2):
        MixerPossibilty = random.uniform(0,1)
        NewChromosome = []
        if MixerPossibilty >= 0.5:
            NewChromosome.append(random.gauss(Chromosome1, Chromosome2 * 0.9))
            NewChromosome.append(random.gauss(Chromosome2, Chromosome1 * 0.9))
        else:
            NewChromosome.append(Chromosome2)
            NewChromosome.append(Chromosome1)
        return NewChromosome
    


# AG = AlgorithmGenetic()
# AG.run()