# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:54:31 2014

@author: igor
"""

import guidata
from guidata.dataset.datatypes import DataSet
from guidata.dataset.dataitems import FloatItem, IntItem
from guidata.qt.QtGui import QSplitter
from guidata.qt.QtCore import Qt
from guidata.dataset.qtwidgets import DataSetEditGroupBox
import matplotlib
matplotlib.use("Qt4Agg")
from matplotlib.backends import backend_qt4agg
from matplotlib import pyplot as plot
import linear_convection_1d


class NumericalInput(DataSet):

    mesh_x_size = IntItem("NX", default=40, min=2, max=401, slider=True)
    wave_speed = FloatItem("Wave Speed", default=1)
    step_size = FloatItem("Step Size", default=5e-3)
    num_of_steps = IntItem("Num. Steps", default=1, min=1, max=300, slider=True)
    
    
class MainWindow(QSplitter):

    def __init__(self, parent=None):
        QSplitter.__init__(self, parent)
        self.setOrientation(Qt.Vertical)
        self.curve = None
        # Set "num_of_steps" as a trigger to update the plot
        NumericalInput.num_of_steps.set_prop("display", callback=self.plot_callback)
        self.numerical_input = DataSetEditGroupBox("Numerical", NumericalInput, show_button=False)
        self.addWidget(self.numerical_input)

        plot.ioff() # Must call plot.draw to update
        self.figure = plot.figure()
        self.plot = self.figure.gca()
        self.addWidget(self.figure.canvas.manager.window)
        
        
    def plot_callback(self, numerical_input, item, value):
        linear_convection_1d.c = numerical_input.wave_speed
        linear_convection_1d.dt = numerical_input.step_size        
        x, u = linear_convection_1d.solve(value)
        self.plot.cla()
        self.plot.plot(x, u)
        plot.draw()
        
        
            

if __name__ == "__main__":
    app = guidata.qapplication()
    inputs = MainWindow()
    inputs.show()
    app.exec_()
