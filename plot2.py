from math import degrees
from operator import truediv
from tkinter.ttk import Notebook
from pyvis.network import Network
import networkx as nx
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from itertools import islice
import random
import numpy as np
import scipy as sc

def areSympomsVisible(infectedNode, simulationParameters):
    if simulationParameters.infectionTime - infectedNode.infectionTimeLeft > simulationParameters.asymptomaticNumber:
        return True

    return False

def drawGraph(graph, infectedNodesIds, deadNodesIds):
    color_map = []
    for node in graph:
        if node in deadNodesIds:
            color_map.append('black')
        elif node in infectedNodesIds: 
            color_map.append('red')
        else:
            color_map.append('green')    

    my_pos = nx.spring_layout(graph, seed = 100)
    nx.draw(graph, pos = my_pos, node_color=color_map, with_labels=True)
    plt.show()

class InfectedNode:
    def __init__(self, id, infectionTimeLeft):
        self.id = id
        self.infectionTimeLeft = infectionTimeLeft

class SimulationParameters:
    def __init__(self):
        self.initInfectedCount = 5
        self.initNodesCount = 300
        self.probalityOfInfectionAfterSymptoms = 0.0
        self.simulationTime = 80
        self.drawGraphEachStep = True
        self.drawPlot = True
        self.asymptomaticNumber = 3
        self.infectionTime = 10

class VirusParameters:
    def __init__(self):
        self.probalityOfInfectionBeforeSymptoms = 0.15
        self.deathProbality = 0.05

        

def runSimulation(simulationParameters, virusParameters):
    G=nx.watts_strogatz_graph(simulationParameters.initNodesCount, 10, 0.1)
    nodes = list(G.nodes)
    initInfectedNodes = random.sample(nodes, simulationParameters.initInfectedCount)
    infectedNodesIds = set()
    infectedNodes = []
    for i in initInfectedNodes:
        infectedNodesIds.add(i)
        infectedNodes.append(InfectedNode(i, simulationParameters.infectionTime))

    deadNodesIds = set()
    immuteNodes = set()

    for currentStep in range(0, simulationParameters.simulationTime):
        curedNodes = []
        deadNodes = []
        infectedNodesSize = len(infectedNodes)

        for infectedNode in islice(infectedNodes, infectedNodesSize):
            #death of notes
            if random.random() < virusParameters.deathProbality:
                deadNodesIds.add(infectedNode.id)
                deadNodes.append(infectedNode)
                continue
                
            #infection of neigbours
            if areSympomsVisible(infectedNode, simulationParameters):
                infectionProbability = simulationParameters.probalityOfInfectionAfterSymptoms
            else:
                infectionProbability = virusParameters.probalityOfInfectionBeforeSymptoms

            for neighbor in G.neighbors(infectedNode.id):
                if neighbor in infectedNodesIds or neighbor in immuteNodes:
                    continue

                if random.random() < infectionProbability:
                    infectedNodes.append(InfectedNode(neighbor, simulationParameters.infectionTime))
                    infectedNodesIds.add(neighbor)

            #decrease infection time left
            infectedNode.infectionTimeLeft -= 1
            if infectedNode.infectionTimeLeft <= 0:
                curedNodes.append(infectedNode)
        
        #remove cured nodes
        for node in curedNodes:
            immuteNodes.add(node.id)
            infectedNodesIds.remove(node.id)
            infectedNodes.remove(node)

        for node in deadNodes:
            infectedNodesIds.remove(node.id)
            infectedNodes.remove(node) 
        
        if(simulationParameters.drawGraphEachStep):
            drawGraph(G, infectedNodesIds, deadNodesIds)

    return len(deadNodesIds)
        


simulationParameters = SimulationParameters()
simulationParameters.drawGraphEachStep = False
virusParameters = VirusParameters()

x = 21

deathProbalities = np.linspace(0, 1, x)
infectionProbabities = np.linspace(0, 1, x)

z = np.zeros([x, x])
for i, deathProbality in enumerate(deathProbalities):
    for j, infectionProbabity in enumerate(infectionProbabities):
        virusParameters.deathProbality = deathProbality
        virusParameters.probalityOfInfectionBeforeSymptoms = infectionProbabity
        zList = []
        for k in range(50):
            zList.append(runSimulation(simulationParameters, virusParameters))

        z[i, j] = sum(zList) / len(zList)
        print("death: ", deathProbality, "inf:", infectionProbabity, "z:", z[i,j])

print(z)


contour = plt.contourf(deathProbalities, infectionProbabities, z, levels = 10)

plt.colorbar(contour)
cbar = plt.colorbar(contour, label='Średnia liczba zgonów')
cbar.set_ticks(contour.levels)
cbar.ax.tick_params(labelsize=20)  # Set the font size for colorbar ticks
cbar.set_label('Średnia liczba zgonów', fontsize=25)  # Set the label size to 16


plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel("Prawdopodobieństwo zarażenia", fontsize=25)
plt.ylabel("Prawdopodobieństwo zgonu", fontsize=25)

plt.show()