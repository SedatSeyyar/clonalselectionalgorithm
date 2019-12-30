from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import sys
import math as m
import numpy as np
import random as r
from MainWindow import Ui_Form

x1min, x2min = 0, 0
x1max, x2max = 0.5, 0.5
populationNumber, iterationNumber = 20, 50
n, beta, theta = 10, 5, 0.3
selectedPopulation = []
lastPopulation = []
population = []


def y(x1, x2):
    temp = ((-30 * (x2 ** 4) + 64 * (x2 ** 3) - 43.8 * (x2 ** 2) + 10.8 * x2 + 0.12) * 1000 * (m.sin(5 * m.pi * x1)) / (
                1 + 0.1 * (x1 ** 2)))
    return np.abs(temp)


def cloning_number(beta, populationNumber, i):
    return int((beta * populationNumber) / i)


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.table = self.ui.tableView
        self.ui.generateInitialPopulationButton.clicked.connect(self.GenerateInitialPopulation)
        self.ui.newProcessButton.clicked.connect(self.NewProcess)
        self.ui.runButton.clicked.connect(self.Run)
        self.ui.newProcessButton.setEnabled(False)
        self.ui.runButton.setEnabled(False)
        self.ui.graphWidget.setBackground('w')

    def GenerateInitialPopulation(self):
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['x1', 'x2', 'Fitness'])
        self.table.setModel(self.model)
        global iterationNumber, populationNumber, n, beta, theta, x1min, x1max, x2min, x2max
        iterationNumber, populationNumber, n, beta, theta = int(self.ui.iterationNumber.text()), int(
            self.ui.initialPopulationNumber.text()), int(self.ui.n.text()), int(self.ui.beta.text()), float(
            self.ui.theta.text())
        temp, temp2, temp_fitness = [], [], []
        np.array(temp)
        np.array(temp2)
        np.array(temp_fitness)
        global population
        for i in range(populationNumber):
            # Step 1 First Popoulation creating
            temp.append(r.uniform(x1min, x1max))
            temp2.append(r.uniform(x2min, x2max))
            # Step 2
            temp_fitness.append(y(temp[i], temp2[i]))
        self.ui.generateInitialPopulationButton.setEnabled(False)
        self.ui.runButton.setEnabled(True)
        population = np.column_stack((temp, temp2))
        population = np.column_stack((population, temp_fitness))
        for i in population:
            row = []
            for item in i:
                cell = QStandardItem(str(item))
                row.append(cell)
            self.model.appendRow(row)
        self.show()
        # Table column resizing
        self.ui.tableView.resizeColumnsToContents()
        # Table data sort
        # self.ui.tableView.sortByColumn(2, 1)
        self.ui.initialPopulationNumber.setEnabled(False)
        self.ui.theta.setEnabled(False)
        self.ui.n.setEnabled(False)
        self.ui.iterationNumber.setEnabled(False)
        self.ui.beta.setEnabled(False)

    def Run(self):
        self.ui.runButton.setEnabled(False)
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['x1', 'x2', 'Fitness'])
        self.table.setModel(self.model)
        plotarray = []
        np.array(plotarray)
        global population, theta, populationNumber, beta, selectedPopulation, lastPopulation, iterationNumber, x1min, x1max, x2min, x2max, n
        for index in range(iterationNumber):
            clon, mutation, clonfitness = [], [], []
            np.array(clon)
            np.array(mutation)
            np.array(clonfitness)
            if len(lastPopulation) > 0:
                temp, temp2, temp_fitness = [], [], []
                np.array(temp)
                np.array(temp2)
                np.array(temp_fitness)
                population = []
                np.array(population)
                for i in range(int(populationNumber / 2)):
                    # Step 1
                    temp.append(r.uniform(x1min, x1max))
                    temp2.append(r.uniform(x2min, x2max))
                    # Step 2
                    temp_fitness.append(y(temp[i], temp2[i]))
                population = np.column_stack((temp, temp2))
                population = np.column_stack((population, temp_fitness))
                population = np.concatenate((lastPopulation, population), axis=0)
            # Step 3 sorting and selecting
            population = population[population[:, 2].argsort()[::-1]]
            selectedPopulation = population[0:n, 0:2]
            # Step 4 Cloning
            for i in range(1, n + 1, 1):
                c = cloning_number(beta, populationNumber, i)
                for k in range(c):
                    clon.append(selectedPopulation[i - 1, 0])
                    clon.append(selectedPopulation[i - 1, 1])
            len_clon = int(len(clon) / 2)
            clon = np.reshape(clon, (len_clon, 2))
            # Step 5 Mutation
            for i in range(len_clon * 2):
                mutation.append(r.uniform(0, 1))
            len_mutation = int(len(mutation) / 2)
            mutation = np.reshape(mutation, (len_mutation, 2))
            if len_clon == len_mutation:
                for i in range(len_clon):
                    if mutation[i, 0] < theta:
                        clon[i, 0] = r.uniform(x1min, x1max)
                    if mutation[i, 1] < theta:
                        clon[i, 1] = r.uniform(x2min, x2max)
            # Step 6
            for i in range(len_clon):
                clonfitness.append(y(clon[i, 0], clon[i, 1]))
            clon = np.column_stack((clon, clonfitness))
            # Step 7 Sorting
            clon = clon[clon[:, 2].argsort()[::-1]]
            # lastPopulation=clon[0:n,0:2] <- Sadece ilk 2 sütünu alır.
            lastPopulation = clon[0:n]
            self.model = QStandardItemModel(self)
            self.model.setHorizontalHeaderLabels(['x1', 'x2', 'Fitness'])
            self.table.setModel(self.model)
            for i in lastPopulation:
                row = []
                for item in i:
                    cell = QStandardItem(str(item))
                    row.append(cell)
                self.model.appendRow(row)
            self.show()
            plotarray.append(index)
            plotarray.append(lastPopulation[0, 2])
        len_plotarray = int(len(plotarray) / 2)
        plotarray = np.reshape(plotarray, (len_plotarray, 2))
        pen = pg.mkPen(color=(150, 150, 150), width=3, style=QtCore.Qt.DotLine)
        self.ui.graphWidget.plot(plotarray[:, 0], plotarray[:, 1], pen=pen)
        self.ui.graphWidget.setLabel('left', 'Value', units='v')
        self.ui.graphWidget.setLabel('bottom', 'Iteration', units='i')
        self.ui.newProcessButton.setEnabled(True)

    def NewProcess(self):
        self.ui.generateInitialPopulationButton.setEnabled(True)
        global selectedPopulation, lastPopulation, population
        selectedPopulation, lastPopulation, population = [], [], []
        self.ui.newProcessButton.setEnabled(False)
        self.model = QStandardItemModel(self)
        self.table.setModel(self.model)
        self.ui.initialPopulationNumber.setEnabled(True)
        self.ui.theta.setEnabled(True)
        self.ui.n.setEnabled(True)
        self.ui.iterationNumber.setEnabled(True)
        self.ui.beta.setEnabled(True)
        self.ui.graphWidget.clear()


def application():
    application = QApplication(sys.argv)
    application.setStyle("Fusion")
    win = App()
    win.show()
    sys.exit(application.exec_())


application()
