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
        self.initInfectedCount = 2
        self.initNodesCount = 10
        self.probalityOfInfectionAfterSymptoms = 0.0
        self.simulationTime = 20
        self.drawGraphEachStep = True
        self.drawPlot = True
        self.asymptomaticNumber = 3
        self.infectionTime = 10

class VirusParameters:
    def __init__(self):
        self.probalityOfInfectionBeforeSymptoms = 0.15
        self.deathProbality = 0.05

        
def runSimulation(simulationParameters, virusParameters):
    G=nx.watts_strogatz_graph(simulationParameters.initNodesCount, 4, 0.1)
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

        y = list(range(0, simulationParameters.initNodesCount))
        x = []
        colors = []
        labels = []
        for i in range(simulationParameters.initNodesCount):
            if i in deadNodesIds:
                colors.append((0, 0, 0))
                labels.append('Nieżywy')
            elif i in immuteNodes:
                colors.append((0, 0, 1))
                labels.append('Odporny')
            elif i in infectedNodesIds:
                colors.append((1, 0,0))
                labels.append('Zarażony')
            else:
                colors.append((0,1,0))
                labels.append('Zdrowy')

            x.append(currentStep + 0.5)
        
        plt.scatter(x, y, marker='|', s=300, linewidth=57, color=colors)

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


    plt.xticks(range(0, 21),fontsize=20)
    plt.yticks(range(0, 10),fontsize=20)
    plt.xlabel("Dzień symulacji", fontsize=25)
    plt.ylabel("Osobnik", fontsize=25)
    plt.xlim((0, 20))
    colorsLegend =  ['green', 'red', 'blue', 'black']
    labelsLegend = ['Zdrowy/podatny', 'Zarażony', 'Ozdrowiały/uodporniony', 'Martwy']
    handles = [plt.scatter([], [], marker='|', s=500, linewidth=23, c=colorsLegend) for colorsLegend in colorsLegend]
    plt.tight_layout()
    plt.legend(handles, labelsLegend, loc='center', bbox_to_anchor=(0.5, -0.21), ncol=len(colors), fontsize = 23)
    plt.show()

    return len(deadNodesIds)
        

simulationParameters = SimulationParameters()
simulationParameters.drawGraphEachStep = False
virusParameters = VirusParameters()

runSimulation(simulationParameters, virusParameters)