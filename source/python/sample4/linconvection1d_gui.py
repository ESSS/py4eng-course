# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:54:31 2014

@author: igor
"""

from guidata.dataset.datatypes import DataSet
from guidata.dataset.dataitems import FloatItem, IntItem
from guidata.qt.QtGui import QSplitter
from guidata.qt.QtCore import Qt
from guidata.dataset.qtwidgets import DataSetEditGroupBox
import matplotlib
matplotlib.use("Qt4Agg")
from matplotlib.backends import backend_qt4agg
from matplotlib import pyplot as plot
import linconvection1d


class NumericalInput(DataSet):
    """
    Numerical Parameters
    Move Num. Steps slider to update the graphic
    """

    mesh_x_size = IntItem("NX", default=40, min=2, max=401, slider=True)
    wave_speed = FloatItem("Wave Speed", default=1)
    step_size = FloatItem("Step Size", default=5e-3)
    num_of_steps = IntItem("Num. Steps", default=1, min=1, max=200, slider=True)
    
    
class MainWindow(QSplitter):

    def __init__(self, parent=None):
        QSplitter.__init__(self, parent)
        self.setOrientation(Qt.Vertical)
        self.curve = None
        plot.ioff() # Must call plot.draw to update
        self.figure = plot.figure()
        self.plot = self.figure.gca()

        # Set "num_of_steps" as a trigger to update the plot
        NumericalInput.num_of_steps.set_prop("display", callback=self.plot_callback)
        self.numerical_input = DataSetEditGroupBox("Numerical", NumericalInput, show_button=False)
        self.addWidget(self.numerical_input)
        self.addWidget(self.figure.canvas.manager.window)
        
        
    def plot_callback(self, numerical_input, item, value):
        linconvection1d.c = numerical_input.wave_speed
        linconvection1d.dt = numerical_input.step_size        
        x, u = linconvection1d.solve(value)
        self.plot.cla()
        self.plot.plot(x, u)
        plot.draw()
