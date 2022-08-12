import numpy as np
from time import sleep

class Neuron:
    def __init__(self,NumberInput):
        self.Wi = []
        self.Xi = []
        for i in range(NumberInput):
            self.Wi.append(np.random.randn())
            self.Xi.append(0)

        self.b = np.random.randn()

        self.result = 0
        self.error = 0
        self.learning_rate = 0.1
            

    def changeRandomWeight(self):
        self.Temp_Wi = []
        for i in range(len(self.Wi)):
            self.Temp_Wi.append(np.random.randn())
        self.Wi = self.Temp_Wi
        self.b = np.random.randn()

    def setInput(self,data):
        self.Xi = data
        self.calcSum()

    def getInput(self):
        return self.Xi

    def getWeight(self):
        return self.Wi + [self.b]
        
    def getOutput(self):
        return self.result

    def Activation(self):
        self.calcSum()
        self.result = self.segmoid(self.result)

    def getError(self):
        return self.error

    def calcSum(self):
        try:
            self.result = self.b
            for i in range(len(self.Wi)):
                self.result += self.Wi[i] * self.Xi[i]
            return True
        except Exception as e:
            return False

    def adaptNeuron(self,Error):
        self.error = Error
        for i in range(len(self.Wi)):
            self.Wi[i] += self.learning_rate * self.error * self.Xi[i]

    def changeWeight(self,NewWeight):
        self.Wi = NewWeight[0:len(self.Wi)]
        self.b = NewWeight[len(self.Wi)]
    
    def segmoid(self,x):
        return 1 / (1 + np.exp(-x))