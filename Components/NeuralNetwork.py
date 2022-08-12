import numpy as np
from Components.Neuron import Neuron

class NeuralNetwork:
    def __init__(self,Layers,FirstLayerInput=2):
        self.NeuronLayer = []

        self.addLayer(Layers[0],FirstLayerInput)
        for i in range(1,len(Layers)):
            self.addLayer(Layers[i],Layers[i-1])

        self.LastInput = []
        self.LastResult = []

    def addLayer(self,NumberNeuron,FirstLayerInput):
        layer = []
        for i in range(NumberNeuron):
            layer.append(Neuron(FirstLayerInput))
        self.NeuronLayer.append(layer)

    def run(self,data):
        self.LastInput = data
        layerData = data
        for layer in self.NeuronLayer:
            layerResult = []
            for neuron in layer:
                neuron.setInput(layerData)
                layerResult.append(self.segmoid(neuron.getOutput()))

            layerData = layerResult
        self.LastResult = layerData
        return layerData

    def getWeight(self):
        weight = []
        for layer in self.NeuronLayer:
            for neuron in layer:
                weight.append(neuron.getWeight())
        return weight

    def changeWeight(self,NewWeight):
        for layer in self.NeuronLayer:
            for neuron in layer:
                neuron.changeWeight(NewWeight.pop(0))

    def GetLastData(self):
        return self.LastInput,self.LastResult
    
    def AdapteError(self,Error):
        for layer in self.NeuronLayer:
            for neuron in layer:
                neuron.adaptNeuron(Error)
                
    def Supervised(self,data,TryNumber=10000):
        self.costs = []
        if len(data) != 0: 
            for i in range(TryNumber):
                rn = np.random.randint(len(data))
                point = data[rn][0]
                GetOutPut = data[rn][1]
                self.run(point)

                First = True
                Last_layer_Error = []
                for layer in reversed(self.NeuronLayer):
                    current_layer_Error = []
                    if First:
                        First = False
                        for j in range(len(layer)):
                            Error = self.segmoid_p(layer[j].getOutput()) * (GetOutPut[j] - self.segmoid(layer[j].getOutput()))
                            current_layer_Error.append(Error)
                            layer[j].adaptNeuron(Error)
                    else:
                        for neuron in layer:
                            outPut = self.segmoid(neuron.getOutput())
                            averageError = 0
                            for j in range(len(Last_layer_Error)):
                                Error = self.segmoid_p(outPut) * Last_layer_Error[j] * outPut
                                averageError += Error

                            averageError /= len(Last_layer_Error)
                            neuron.adaptNeuron(averageError)
                            current_layer_Error.append(averageError)
                    Last_layer_Error = current_layer_Error
                self.costs.append(self.cost(data[rn]))
        
# return np.square(data[2] - self.run(data[:-1])[0])
    def cost(self,data):
        GetOutPut = data[1]
        Sum = 0
        for i in range(len(GetOutPut)):
            Sum += np.square(GetOutPut[i] - self.run(data[0])[i])
        return Sum / len(GetOutPut)

    def segmoid(self,x):
        return 1 / (1 + np.exp(-x))

    def segmoid_p(self,x):
        return self.segmoid(x) * (1 - self.segmoid(x))


