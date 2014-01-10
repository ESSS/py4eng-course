from guidata.dataset.datatypes import DataSet
from guidata.dataset.dataitems import FloatItem
from guidata.qt.QtGui import QSplitter
from guidata.qt.QtCore import Qt, SIGNAL
from guidata.dataset.qtwidgets import DataSetEditGroupBox
from matplotlib import pyplot as plot
import guidata
import ansys_opt

class OptimizationInput(DataSet):
    
    stress_ratio = FloatItem('Stress Ratio', default=3)
    copper_initial = FloatItem('Copper Initial Cross-section',
                               min=0.1, max=1.0, default=0.5)
    steel_initial = FloatItem('Steel Initial Cross-section',
                               min=0.1, max=1.0, default=0.5)


class MainWindow(QSplitter):

    def __init__(self, parent=None):
        QSplitter.__init__(self, parent)
        self.setOrientation(Qt.Vertical)
        self.optimization_input = DataSetEditGroupBox("Optimization", OptimizationInput)
        self.addWidget(self.optimization_input)
        self.connect(self.optimization_input, SIGNAL("apply_button_clicked()"), self.start_opt)
        
        plot.ioff()
        figure = plot.figure()
        self.addWidget(figure.canvas.manager.window)
        
        
    def start_opt(self):
        ansys_opt.stress_ratio = self.optimization_input.dataset.stress_ratio
        ansys_opt.optimize()    
    

app = guidata.qapplication()
inputs = MainWindow()
inputs.show()
app.exec_()